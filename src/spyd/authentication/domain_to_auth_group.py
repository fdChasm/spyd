def domain_to_auth_group(domain):
    ns_parts = domain.split('.')
    ns_parts.reverse()
    ns_parts.append('auth')
    return '.'.join(ns_parts)
