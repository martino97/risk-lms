"""
LDAP/Active Directory Authentication Backend for Risk LMS
Domain: KCBLTZ.CRDBBANKPLC.COM
DNS Servers: 192.168.10.50 (primary), 192.168.10.10 (alternate)

Users login with username only (e.g., JLugome, MMalopa)
Full names are retrieved from AD (e.g., Jasmin Lugome, Martin Malopa)

Based on PHP implementation using simple bind with username@domain format.
"""
import ldap3
from ldap3 import Server, Connection, ALL, SIMPLE, SUBTREE
from ldap3.core.exceptions import LDAPException, LDAPBindError
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

# LDAP Configuration - matching PHP implementation
LDAP_SERVERS = [
    '192.168.10.50',  # Primary DNS (ldap_host in PHP)
    '192.168.10.10',  # Alternate DNS
]
LDAP_DOMAIN = 'kcbltz.crdbbankplc.com'  # ldap_domain in PHP
LDAP_BASE_DN = 'DC=kcbltz,DC=crdbbankplc,DC=com'
LDAP_PORT = 389  # Default LDAP port (ldap_port in PHP)
LDAP_USE_SSL = False


class LDAPBackend(BaseBackend):
    """
    Custom authentication backend for Active Directory/LDAP.
    Users login with their domain username (sAMAccountName) like JLugome, MMalopa.
    
    Mimics PHP ldap_bind($ldap_connection, "$un@$ldap_domain", $pw) approach.
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate user against Active Directory.
        
        Args:
            username: Domain username (sAMAccountName) e.g., JLugome, MMalopa
            password: User's domain password
        
        Returns:
            User object if authentication successful, None otherwise
        """
        if not username or not password:
            return None
        
        # Clean the username - remove any domain prefix or extra characters
        username = self._clean_username(username)
        
        # Try to authenticate against LDAP
        ldap_user_info = self._ldap_authenticate(username, password)
        
        if ldap_user_info:
            # Get or create local user
            user = self._get_or_create_user(ldap_user_info)
            return user
        
        return None
    
    def get_user(self, user_id):
        """Retrieve user by ID"""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
    
    def _clean_username(self, username):
        """
        Clean and normalize the username input.
        Users enter just their username like: JLugome, MMalopa
        """
        # Remove any whitespace
        username = username.strip()
        
        # Remove domain prefix if present (KCBLTZ\username)
        if '\\' in username:
            username = username.split('\\')[-1]
        
        # If user accidentally entered email format, extract username
        if '@' in username:
            username = username.split('@')[0]
        
        return username
    
    def _ldap_authenticate(self, username, password):
        """
        Authenticate against Active Directory servers.
        
        Uses simple bind with username@domain format, matching PHP:
        ldap_bind($ldap_connection, "$un@$ldap_domain", $pw)
        
        Args:
            username: sAMAccountName like JLugome, MMalopa
            password: Domain password
        
        Returns dict with user info if successful, None otherwise.
        """
        for server_ip in LDAP_SERVERS:
            try:
                logger.info(f"Attempting LDAP connection to {server_ip}")
                
                # Create server connection (equivalent to ldap_connect in PHP)
                server = Server(
                    server_ip,
                    port=LDAP_PORT,
                    use_ssl=LDAP_USE_SSL,
                    get_info=ALL,
                    connect_timeout=10
                )
                
                # Bind using username@domain format (same as PHP: "$un@$ldap_domain")
                bind_user = f"{username}@{LDAP_DOMAIN}"
                
                logger.info(f"Attempting bind as: {bind_user}")
                
                # Create connection with SIMPLE authentication
                # This matches PHP's ldap_bind behavior
                conn = Connection(
                    server,
                    user=bind_user,
                    password=password,
                    authentication=SIMPLE,
                    auto_bind=False,
                    raise_exceptions=False,
                    read_only=True
                )
                
                # Set LDAP options (matching PHP's ldap_set_option)
                # LDAP_OPT_PROTOCOL_VERSION = 3
                # LDAP_OPT_REFERRALS = 0
                
                # Attempt to bind (authenticate)
                if conn.bind():
                    logger.info(f"LDAP bind successful for {username}")
                    
                    # Search for user details to get full name, department, etc.
                    user_info = self._search_user(conn, username)
                    conn.unbind()
                    
                    if user_info:
                        return user_info
                    
                    # If search failed but bind succeeded, return basic info
                    return {
                        'username': username,
                        'email': f"{username}@cbtbank.co.tz",
                        'first_name': '',
                        'last_name': '',
                        'department': '',
                        'title': '',
                        'phone': '',
                        'groups': [],
                        'role': 'banker',
                    }
                else:
                    logger.debug(f"LDAP bind failed for {username}: {conn.result}")
                    # Try next server
                    continue
                
            except LDAPBindError as e:
                logger.debug(f"LDAP bind error for {username} on {server_ip}: {e}")
                continue
            except Exception as e:
                logger.warning(f"Could not connect to LDAP server {server_ip}: {e}")
                continue
        
        logger.warning(f"LDAP authentication failed for {username} on all servers")
        return None
    
    def _search_user(self, conn, username):
        """
        Search for user details in Active Directory by sAMAccountName.
        
        Args:
            username: sAMAccountName like JLugome, MMalopa
        
        Returns dict with user attributes if found.
        """
        # Search by sAMAccountName (the login username)
        search_filter = f"(sAMAccountName={username})"
        
        # Attributes to retrieve from AD
        attributes = [
            'sAMAccountName',      # Login username (JLugome)
            'userPrincipalName',   # UPN if available
            'mail',                # Email if available
            'givenName',           # First name (Jasmin)
            'sn',                  # Surname/Last name (Lugome)
            'displayName',         # Full display name
            'department',          # Department
            'title',               # Job title
            'telephoneNumber',     # Phone
            'memberOf',            # AD Groups
        ]
        
        def get_attr_value(entry, attr_name):
            """Safely get attribute value, handling empty arrays and None"""
            if hasattr(entry, attr_name):
                val = getattr(entry, attr_name)
                if val and val.value:
                    # Handle single value or list
                    if isinstance(val.value, list):
                        return str(val.value[0]) if val.value else ''
                    return str(val.value)
            return ''
        
        try:
            conn.search(
                search_base=LDAP_BASE_DN,
                search_filter=search_filter,
                search_scope=SUBTREE,
                attributes=attributes
            )
            
            if conn.entries:
                entry = conn.entries[0]
                
                # Extract sAMAccountName
                sam_account = get_attr_value(entry, 'sAMAccountName') or username
                
                # Extract first and last name
                first_name = get_attr_value(entry, 'givenName')
                last_name = get_attr_value(entry, 'sn')
                
                # If no first/last name, try to parse from displayName
                if not first_name and not last_name:
                    display_name = get_attr_value(entry, 'displayName')
                    if display_name:
                        name_parts = display_name.split()
                        if len(name_parts) >= 2:
                            first_name = name_parts[0]
                            last_name = ' '.join(name_parts[1:])
                        elif len(name_parts) == 1:
                            first_name = name_parts[0]
                
                # Get email from AD or generate from names
                email = get_attr_value(entry, 'mail')
                if not email:
                    # Generate email from names: Jasmin.Lugome@crdbbank.co.tz
                    if first_name and last_name:
                        # Clean names for email (remove middle initials, etc.)
                        clean_first = first_name.split()[0] if first_name else ''
                        clean_last = last_name.split()[-1] if last_name else ''
                        email = f"{clean_first}.{clean_last}@crdbbank.co.tz"
                    else:
                        email = f"{sam_account}@crdbbank.co.tz"
                
                # Extract department and title
                department = get_attr_value(entry, 'department')
                title = get_attr_value(entry, 'title')
                phone = get_attr_value(entry, 'telephoneNumber')
                
                # Get group memberships
                groups = []
                if hasattr(entry, 'memberOf') and entry.memberOf:
                    groups = [str(g) for g in entry.memberOf.values] if hasattr(entry.memberOf, 'values') else []
                
                # Extract user info
                user_info = {
                    'username': sam_account,
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'department': department,
                    'title': title,
                    'phone': phone,
                    'groups': groups,
                }
                
                # Determine role based on title or groups
                user_info['role'] = self._determine_role(user_info)
                
                logger.info(f"Found LDAP user: {user_info['username']} ({user_info['first_name']} {user_info['last_name']}) with role: {user_info['role']}")
                return user_info
                
        except Exception as e:
            logger.error(f"LDAP search error: {e}")
        
        # Return basic info if search failed but bind succeeded
        # This means the user authenticated but we couldn't get their details
        return {
            'username': username,
            'email': f"{username}@cbtbank.co.tz",
            'first_name': '',
            'last_name': '',
            'department': '',
            'title': '',
            'phone': '',
            'groups': [],
            'role': 'banker',  # Default role
        }
    
    def _determine_role(self, user_info):
        """
        Determine user role based on AD attributes (title, groups, department).
        
        Roles:
        - head_of_risk: Head of Risk Management
        - risk_compliance_specialist: Risk & Compliance Specialist
        - banker: Regular banker (default)
        """
        title = user_info.get('title', '').lower()
        department = user_info.get('department', '').lower()
        groups = [g.lower() for g in user_info.get('groups', [])]
        
        # Check for Head of Risk
        head_keywords = ['head of risk', 'risk manager', 'chief risk', 'cro', 'risk director']
        for keyword in head_keywords:
            if keyword in title:
                return 'head_of_risk'
        
        # Check AD groups for Head of Risk
        head_groups = ['risk_heads', 'risk management heads', 'risk_managers']
        for group in groups:
            for hg in head_groups:
                if hg in group:
                    return 'head_of_risk'
        
        # Check for Risk Compliance Specialist
        specialist_keywords = ['risk compliance', 'compliance specialist', 'risk specialist', 
                              'risk analyst', 'compliance officer', 'risk officer']
        for keyword in specialist_keywords:
            if keyword in title:
                return 'risk_compliance_specialist'
        
        # Check department for risk roles
        if 'risk' in department or 'compliance' in department:
            specialist_dept_keywords = ['specialist', 'analyst', 'officer']
            for keyword in specialist_dept_keywords:
                if keyword in title:
                    return 'risk_compliance_specialist'
        
        # Check AD groups for Risk Compliance Specialist
        specialist_groups = ['risk_compliance', 'compliance_team', 'risk_team']
        for group in groups:
            for sg in specialist_groups:
                if sg in group:
                    return 'risk_compliance_specialist'
        
        # Default to banker
        return 'banker'
    
    def _get_or_create_user(self, ldap_user_info):
        """
        Get existing user or create new one from LDAP info.
        Uses username (sAMAccountName) as the primary identifier.
        Updates user info on each login to keep in sync with AD.
        """
        username = ldap_user_info['username']
        email = ldap_user_info['email']
        
        try:
            # Find by username first (sAMAccountName is the primary identifier)
            user = User.objects.get(username__iexact=username)
            logger.info(f"Found existing user by username: {username}")
        except User.DoesNotExist:
            try:
                # Try to find by email as fallback
                user = User.objects.get(email__iexact=email)
                logger.info(f"Found existing user by email: {email}")
            except User.DoesNotExist:
                # Create new user
                user = User(
                    username=username,
                    email=email,
                )
                logger.info(f"Creating new user from LDAP: {username}")
        
        # Update user info from LDAP (sync on each login)
        user.email = email  # Update email in case it changed
        user.first_name = ldap_user_info.get('first_name', '') or user.first_name
        user.last_name = ldap_user_info.get('last_name', '') or user.last_name
        user.department = ldap_user_info.get('department', '') or user.department
        user.phone = ldap_user_info.get('phone', '') or user.phone
        user.role = ldap_user_info.get('role', 'banker')
        
        # Set unusable password for LDAP users (they auth via AD)
        user.set_unusable_password()
        user.is_active = True
        
        user.save()
        
        logger.info(f"User synced: {user.username} - {user.get_full_name()} ({user.role})")
        
        return user


class LDAPSimpleBackend(BaseBackend):
    """
    Simplified LDAP backend for basic authentication.
    Use this if NTLM is not available.
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None
        
        # Clean username
        if '@' not in username:
            # Add domain if not present
            upn = f"{username}@{LDAP_DOMAIN}"
        else:
            upn = username
        
        for server_ip in LDAP_SERVERS:
            try:
                server = Server(server_ip, port=LDAP_PORT, use_ssl=LDAP_USE_SSL, get_info=ALL)
                conn = Connection(server, user=upn, password=password)
                
                if conn.bind():
                    logger.info(f"Simple LDAP bind successful for {username}")
                    
                    # Get or create user
                    email = upn if '@' in upn else f"{username}@cbtbank.co.tz"
                    user, created = User.objects.get_or_create(
                        email__iexact=email,
                        defaults={
                            'username': username.split('@')[0] if '@' in username else username,
                            'email': email,
                            'role': 'banker',
                        }
                    )
                    
                    if created:
                        user.set_unusable_password()
                        user.save()
                        logger.info(f"Created new user from LDAP: {email}")
                    
                    conn.unbind()
                    return user
                    
            except Exception as e:
                logger.warning(f"Simple LDAP auth error on {server_ip}: {e}")
                continue
        
        return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
