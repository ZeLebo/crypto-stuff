from certificate import Certificate

def build_chain(target_owner, certificates) -> list:
    """
    Build a chain of certificates from the target owner to the root

    :param target_owner: owner for whom the chain is built
    :param certificates: list of certificates {owner: certificate_object}
    
    :return chain of certificates to the root from owner, None if not found
    """

    chain = []
    current_owner = target_owner

    while current_owner in certificates:
        cert = certificates[current_owner]
        chain.append(cert)

        if cert.is_root:
            return chain[::-1]
        
        else:
            current_owner = cert.issuer
            if current_owner not in certificates:
                print(f"Certificate for {current_owner} not found")
                return None

    print (f"Target owner {target_owner} not found in the chain")
    return None

def hierarcial_run():
    print("hierarcial PKI")

    certificates = {
        "root": Certificate("root", None, True),
        "ca_1": Certificate("ca_1", "root")
    }

    print("Chain for user 2")
    chain_user2 = build_chain("user_2", certificates)
    if chain_user2:
        for cert in chain_user2:
            print(cert)
    else:
        print("Chain not found")

    print("fixing the user")

    certificates["ca_2"] = Certificate("ca_2", "ca_1")
    certificates["user_1"] = Certificate("user_1", "ca_1")
    certificates["user_2"] = Certificate("user_2", "ca_2")
    
    chain_user2 = build_chain("user_2", certificates)
    if chain_user2:
        for cert in chain_user2:
            print(cert)
    else:
        print("Chain not found")

    from PrettyPrint import PrettyPrintTree

    pt = PrettyPrintTree(lambda x: x.assignee, lambda x: x.owner)
    pt(certificates)


if __name__ == "__main__":
    hierarcial_run()