/**
 * SCORM 1.2 and 2004 API Wrapper for Risk LMS
 * This wrapper intercepts SCORM calls from Captivate/Articulate courses
 * and communicates with the Django backend to track progress
 */

(function() {
    'use strict';
    
    // Configuration - will be set by the parent page
    window.SCORM_CONFIG = window.SCORM_CONFIG || {
        interactiveId: null,
        csrfToken: null,
        progressUrl: null,
        totalSlides: 0,
        debug: false
    };
    
    // SCORM data storage
    var scormData = {
        'cmi.core.lesson_location': '',
        'cmi.core.lesson_status': 'not attempted',
        'cmi.core.score.raw': '',
        'cmi.core.score.min': '0',
        'cmi.core.score.max': '100',
        'cmi.core.session_time': '0000:00:00',
        'cmi.core.total_time': '0000:00:00',
        'cmi.suspend_data': '',
        'cmi.core.exit': '',
        'cmi.core.entry': 'ab-initio',
        'cmi.core.student_id': '',
        'cmi.core.student_name': '',
        // SCORM 2004
        'cmi.location': '',
        'cmi.completion_status': 'not attempted',
        'cmi.success_status': 'unknown',
        'cmi.score.scaled': '',
        'cmi.score.raw': '',
        'cmi.progress_measure': ''
    };
    
    // Track current state
    var currentSlide = 0;
    var highestSlideReached = 0;
    var initialized = false;
    var lastError = 0;
    
    // Debug logging
    function log(message, data) {
        if (window.SCORM_CONFIG.debug) {
            console.log('[SCORM API]', message, data || '');
        }
        // Also send to parent window
        if (window.parent && window.parent !== window) {
            window.parent.postMessage({
                type: 'scormLog',
                message: message,
                data: data
            }, '*');
        }
    }
    
    // Send progress update to server
    function sendProgressUpdate(slideNumber, additionalData) {
        if (!window.SCORM_CONFIG.progressUrl) {
            log('No progress URL configured');
            return;
        }
        
        var data = Object.assign({
            current_slide: slideNumber,
            highest_slide_reached: highestSlideReached,
            completion_percentage: Math.round((highestSlideReached / window.SCORM_CONFIG.totalSlides) * 100),
            total_slides: window.SCORM_CONFIG.totalSlides,
            scorm_data: scormData
        }, additionalData || {});
        
        // Send to parent window first (real-time UI update)
        if (window.parent && window.parent !== window) {
            window.parent.postMessage({
                type: 'slideChange',
                slideNumber: slideNumber,
                highestSlideReached: highestSlideReached,
                data: data
            }, '*');
        }
        
        // Then send to server
        fetch(window.SCORM_CONFIG.progressUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': window.SCORM_CONFIG.csrfToken
            },
            body: JSON.stringify(data)
        })
        .then(function(response) { return response.json(); })
        .then(function(result) {
            log('Progress saved', result);
        })
        .catch(function(error) {
            log('Progress save failed', error);
        });
    }
    
    // Parse lesson_location to extract slide number
    function parseSlideNumber(location) {
        if (!location) return 0;
        
        // Try different formats that Captivate might use
        var slideNum = 0;
        
        // Format: "1" or "5" (just a number)
        if (/^\d+$/.test(location)) {
            slideNum = parseInt(location, 10);
        }
        // Format: "slide_5" or "Slide5"
        else if (/slide[_]?(\d+)/i.test(location)) {
            var match = location.match(/slide[_]?(\d+)/i);
            slideNum = parseInt(match[1], 10);
        }
        // Format: "m1s5" (module 1 slide 5) - common in Captivate
        else if (/m\d+s(\d+)/i.test(location)) {
            var match = location.match(/m\d+s(\d+)/i);
            slideNum = parseInt(match[1], 10);
        }
        // Format with frame number
        else if (/frame[_]?(\d+)/i.test(location)) {
            var match = location.match(/frame[_]?(\d+)/i);
            slideNum = parseInt(match[1], 10);
        }
        
        return slideNum || 0;
    }
    
    // ============================================
    // SCORM 1.2 API (API object)
    // ============================================
    var API = {
        LMSInitialize: function(param) {
            log('LMSInitialize', param);
            initialized = true;
            lastError = 0;
            
            // Notify parent
            if (window.parent && window.parent !== window) {
                window.parent.postMessage({ type: 'scormInitialize' }, '*');
            }
            
            return 'true';
        },
        
        LMSFinish: function(param) {
            log('LMSFinish', param);
            
            // Send final progress
            sendProgressUpdate(currentSlide, {
                finished: true
            });
            
            // Notify parent
            if (window.parent && window.parent !== window) {
                window.parent.postMessage({ type: 'scormFinish' }, '*');
            }
            
            initialized = false;
            return 'true';
        },
        
        LMSGetValue: function(element) {
            log('LMSGetValue', element);
            lastError = 0;
            
            if (scormData.hasOwnProperty(element)) {
                return scormData[element];
            }
            
            lastError = 401; // Not implemented
            return '';
        },
        
        LMSSetValue: function(element, value) {
            log('LMSSetValue', element + ' = ' + value);
            lastError = 0;
            
            scormData[element] = value;
            
            // Handle lesson_location (slide tracking)
            if (element === 'cmi.core.lesson_location' || element === 'cmi.location') {
                var slideNum = parseSlideNumber(value);
                if (slideNum > 0) {
                    currentSlide = slideNum;
                    if (slideNum > highestSlideReached) {
                        highestSlideReached = slideNum;
                    }
                    sendProgressUpdate(slideNum);
                }
            }
            
            // Handle completion status
            if (element === 'cmi.core.lesson_status' || element === 'cmi.completion_status') {
                if (value === 'completed' || value === 'passed') {
                    sendProgressUpdate(currentSlide, {
                        content_completed: true
                    });
                    
                    // Notify parent
                    if (window.parent && window.parent !== window) {
                        window.parent.postMessage({ 
                            type: 'complete',
                            completed: true
                        }, '*');
                    }
                }
            }
            
            // Handle score
            if (element === 'cmi.core.score.raw' || element === 'cmi.score.raw' || element === 'cmi.score.scaled') {
                var score = parseFloat(value);
                if (element === 'cmi.score.scaled') {
                    score = score * 100; // Convert 0-1 to 0-100
                }
                
                sendProgressUpdate(currentSlide, {
                    quiz_score: score
                });
                
                // Notify parent
                if (window.parent && window.parent !== window) {
                    window.parent.postMessage({ 
                        type: 'quizScore',
                        score: score
                    }, '*');
                }
            }
            
            return 'true';
        },
        
        LMSCommit: function(param) {
            log('LMSCommit', param);
            // Save current state
            sendProgressUpdate(currentSlide);
            return 'true';
        },
        
        LMSGetLastError: function() {
            return String(lastError);
        },
        
        LMSGetErrorString: function(errorCode) {
            var errors = {
                '0': 'No error',
                '101': 'General exception',
                '201': 'Invalid argument error',
                '202': 'Element cannot have children',
                '203': 'Element not an array',
                '301': 'Not initialized',
                '401': 'Not implemented error',
                '402': 'Invalid set value',
                '403': 'Element is read only',
                '404': 'Element is write only',
                '405': 'Incorrect data type'
            };
            return errors[errorCode] || 'Unknown error';
        },
        
        LMSGetDiagnostic: function(errorCode) {
            return this.LMSGetErrorString(errorCode);
        }
    };
    
    // ============================================
    // SCORM 2004 API (API_1484_11 object)
    // ============================================
    var API_1484_11 = {
        Initialize: function(param) {
            return API.LMSInitialize(param);
        },
        
        Terminate: function(param) {
            return API.LMSFinish(param);
        },
        
        GetValue: function(element) {
            return API.LMSGetValue(element);
        },
        
        SetValue: function(element, value) {
            return API.LMSSetValue(element, value);
        },
        
        Commit: function(param) {
            return API.LMSCommit(param);
        },
        
        GetLastError: function() {
            return API.LMSGetLastError();
        },
        
        GetErrorString: function(errorCode) {
            return API.LMSGetErrorString(errorCode);
        },
        
        GetDiagnostic: function(errorCode) {
            return API.LMSGetDiagnostic(errorCode);
        }
    };
    
    // ============================================
    // Captivate-specific API extensions
    // ============================================
    
    // Some Captivate versions look for these
    API.version = '1.0';
    API_1484_11.version = '1.0';
    
    // ============================================
    // Expose APIs globally
    // ============================================
    window.API = API;
    window.API_1484_11 = API_1484_11;
    
    // Also expose for frames
    if (window.parent && window.parent !== window) {
        try {
            window.parent.API = API;
            window.parent.API_1484_11 = API_1484_11;
        } catch (e) {
            // Cross-origin restriction, that's OK
        }
    }
    
    log('SCORM API Wrapper loaded and ready');
    
})();
