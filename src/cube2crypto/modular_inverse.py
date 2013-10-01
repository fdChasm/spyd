from extended_euclidean_gcd import extended_euclidean_gcd

def modular_inverse(a, m):
    """Copied from
    http://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm"""
    g, x, _ = extended_euclidean_gcd(a, m)
    if g != 1:
        return None  # modular inverse does not exist
    else:
        return x % m
