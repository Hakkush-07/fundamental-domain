from random import random
from fundamental_domain.sl2z import Gamma, fundamental_domain_to_asy, fundamental_domain_to_tex

def main(pdf=False):
    def fn(n):
        def f(m):
            return m.c % n == 0
        return f
    gamma = Gamma(fn(17))

    # select randomly from the available options
    def select_random(cri_cr_typ_m):
        return random()
    
    # selects biggest possible option
    def select_appearance(cri_cr_typ_m):
        return cri_cr_typ_m[-1].appearance()
    
    # selects the option with the least distance
    def select_distance(cri_cr_typ_m):
        return -cri_cr_typ_m[-1].distance
    
    # selects biggest possible option, random if equal
    def select_appearance_random(cri_cr_typ_m):
        return cri_cr_typ_m[-1].appearance() + 0.001 * random()
    
    # selects the option with the least distance, random if equal
    def select_distance_random(cri_cr_typ_m):
        return -cri_cr_typ_m[-1].distance + 0.001 * random()
    
    fundamental_domain = gamma.get_fundamental_domain(select_appearance_random)

    with open("main.tex", "w+") as file:
        file.write(fundamental_domain_to_tex(fundamental_domain))

    with open("main.asy", "w+") as file:
        file.write(fundamental_domain_to_asy(fundamental_domain))

    if pdf:
        from subprocess import run
        run(["pdflatex", "-jobname", "main-tex", "main.tex"])
        run(["asy", "main.asy", "-o", "main-asy"])

if __name__ == "__main__":
    main(pdf=True)
