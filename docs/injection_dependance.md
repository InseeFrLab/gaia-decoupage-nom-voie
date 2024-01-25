## Injection de dépendance

Le framework retenu pour l'injection de dépendance est injector.
[documentation](https://injector.readthedocs.io/en/latest/index.html)
[github](https://github.com/alecthomas/injector)

Il reste simple et permet l'injection sur les besoins d'une architecture hexagonale.

En partant de l'exemple, dans le domain, action1_copie_rfs, action1_copierfs_usecase.py :
la classe CopierRfsUseCase possède un constructeur :

````python
@inject
def __init__(self, rfs_repository :RfsRepositoryInterface ) -> None:
        self.rfs_repository = rfs_repository
````

Le décorateur @inject, va chercher une instance de chaque paramètres du constructeur ( hormis self) pour l'injecter au moment de la construction de l'objet ( il est possible de definir des parametres non injectable). Ainsi on résoud les dépendances.

On note, cependant ici, que l'argument du constructeur prend un type "interface" RfsRepositoryInterface, qui correspond à l'interface connue du use case afin de ne pas réaliser de couplage avec d'autres couches de l'architecture. Cette interface doit être implémentée et l'injection doit injecter l'implémentation de l'interface.
En python, les interfaces ressemblent beaucoup plus aux classes abstraites avec méthodes virtuelles pures de C++. c'est à dire que l'on déclare les signatures des méthodes en indiquant dans la classe qu'il n'y a pas d'implémentation dans l'interface.

une autre façon plus légère de faire :

````python
@inject
@dataclass
class AdapterModule(Module):
    ''' ici on cherche à parametrer le module d'injection pour la partie adapter de l'application'''
        
    filerepository: FileRfsRepositoryAdapter

````

Le décorateur @dataclass génère le constructeur tout seul en partant des champs déclarés de l'objet, ici filerepository. L'injection fonctionne ensuite comme précédemment.

L'implémentation est dans le package application.adapter, au sein du fichier rfs_repository_file_adapter.py.
La classe implémente l'interface :

````python
class FileRfsRepositoryAdapter(RfsRepositoryInterface)

````
En python , pour instancier cette classe qui hérite, il faut implémenter toutes les méthodes abstraites de l'interface.
Il n'y a pas d'élément à décorer pour l'injection de dépendance.

Afin d'indiquer à l'injection de dépendance, que lorsqu'il trouve le type interface, il injecte une implementation ( concept nommé binding), un module dédié à tout le package adapter à été fait.
dans le package application, adapter, le fichier adapter_module.py contient le binding pour l'interface précédente :

````python
@inject
@dataclass
class AdapterModule(Module):
    ''' ici on cherche à paramétrer le module d'injection pour la partie adapter de l'application'''
        
    filerepository: FileRfsRepositoryAdapter

    @singleton
    @provider
    def provide_rfs_repository_adapter(self) -> RfsRepositoryInterface:
        ''' la méthode permet de matcher le type de l'interface attendu par le domain en type de l'adapter.'''
        return self.filerepository

````

On déclare un fournisseur (provider) du type RfsReposirotyInterface avec le décorateur @provider. Ceci, créé un fournisseur du type, une méthode capable de fabriquer l'objet et l'inscrit dans le framework.
Ce provider ici retourne simplement l'instance filerepository d'un autre type et la bind avec le type RfsRepositoryInterface.
Le décorateur @singleton déclare qu'il n'y aura qu'une seule instance possible de RfsRepositoryInterface, ceci ressemble au fonctionnement spring mais dépend du cas d'usage, le singleton n'est pas toujours adapté.

Dernière étape, il faut déclarer ce module AdapterModule dans l'application. Dans le main.py, l’adapteur module est déclaré comme pris en charge par l'injector :

````python
def injection_configuration(self):
    injector = Injector([AdapterModule()])

if __name__ == '__main__':
    injection_configuration()
````
