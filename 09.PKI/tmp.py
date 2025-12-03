from PrettyPrint import PrettyPrintTree


class Certificate:
    def __init__(self, owner, issuer, is_root=False):
        self.owner = owner
        self.issuer = issuer
        self.is_root = is_root
        self.issued_by_me = []

    def __repr__(self):
        return self.owner


def build_chain(target_owner, certificates_map) -> list:
    """
    Build a chain of certificates from the target owner to the root

    :param target_owner: owner for whom the chain is built
    :param certificates_map: dictionary of certificates {owner: certificate_object}

    :return chain of certificates to the root from owner, None if not found
    """

    chain = []
    current_owner = target_owner

    while current_owner in certificates_map:
        cert = certificates_map[current_owner]
        chain.append(cert)

        if cert.is_root:
            return chain[::-1]

        else:
            current_owner = cert.issuer
            if current_owner not in certificates_map:
                print(f"Certificate for issuer '{
                      current_owner}' not found (chain for '{target_owner}' is broken).")
                return None

    print(f"Target owner '{target_owner}' not found in the certificates map.")
    return None


class PKINode:
    def __init__(self, certificate):
        self.certificate = certificate
        self.children = []

    def get_children(self):
        return self.children

    def get_value(self):
        return self.certificate.owner

    def add_child(self, child_node):
        self.children.append(child_node)


def build_pki_tree(certificates_map):
    """
    Строит древовидную структуру PKI из плоского словаря сертификатов.
    Возвращает корневой узел дерева.
    """
    nodes = {owner: PKINode(cert) for owner, cert in certificates_map.items()}
    root_node = None

    for owner, node in nodes.items():
        if node.certificate.is_root:
            root_node = node
        elif node.certificate.issuer in nodes:
            nodes[node.certificate.issuer].add_child(node)
        else:
            print(f"Warning: Issuer '{node.certificate.issuer}' for '{
                  node.certificate.owner}' not found in the system. Node will not be part of the main tree.")

    return root_node


def hierarcial_run():
    print("--- Иерархическая PKI ---")

    certificates_map = {
        "root": Certificate("root", None, True),
        "ca_1": Certificate("ca_1", "root"),
        "user_1": Certificate("user_1", "ca_1")
    }

    print("\nЦепочка для 'user_1' (начальная конфигурация):")
    chain_user1 = build_chain("user_1", certificates_map)
    if chain_user1:
        for cert in chain_user1:
            print(cert.owner)
    else:
        print("Цепочка не найдена.")

    print("\nРасширяем PKI:")
    certificates_map["ca_2"] = Certificate("ca_2", "ca_1")
    certificates_map["user_2"] = Certificate("user_2", "ca_2")
    certificates_map["ca_3"] = Certificate("ca_3", "root")
    certificates_map["user_3"] = Certificate("user_3", "ca_3")
    certificates_map["user_4"] = Certificate("user_4", "ca_3")

    print("\nЦепочка для 'user_2' (расширенная конфигурация):")
    chain_user2 = build_chain("user_2", certificates_map)
    if chain_user2:
        for cert in chain_user2:
            print(cert.owner)
    else:
        print("Цепочка не найдена.")

    print("\nВизуализация иерархической PKI:")
    pki_tree_root = build_pki_tree(certificates_map)

    if pki_tree_root:
        pt = PrettyPrintTree(lambda x: x.get_children(),
                             lambda x: x.get_value())
        pt(pki_tree_root)
    else:
        print("Не удалось построить корневой узел для визуализации PKI.")


if __name__ == "__main__":
    hierarcial_run()
