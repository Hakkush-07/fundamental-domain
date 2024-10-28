from random import random
from fundamental_domain.sl2z import Gamma, fundamental_domain_to_asy, fundamental_domain_to_tex

def main(pdf=False):
    gamma = Gamma.sl2z()
    gamma = Gamma.gamma_1_n(5)
    
    fundamental_domain = gamma.get_fundamental_domain(lambda cr: -cr.distance) #  + 0.001 * random(), cr.appearance()

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
