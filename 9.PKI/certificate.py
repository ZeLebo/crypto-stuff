class Certificate:
    def __init__(self, owner, issuer, is_root=False):
        self.owner = owner
        self.issuer = issuer
        self.is_root = is_root

    def __repr__(self):
        if self.is_root:
            return f"Certificate(owner={self.owner}, Type=Root)"
        return f"Certificate(owner={self.owner}, issuer={self.issuer})"
    