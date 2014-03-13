# SaveFTP

Le script saveftp permet de sauvegarder le contenu d'une arborescence au sein d'une archive zip. L'archive sera ensuite stockée sur un serveur distant via un transfert FTP.

## Comment l'utiliser

`saveftp.py chemin hote[:port] [-u|--user username [-p|--password password]]`

### Les paramètres obligatoires

La syntaxe minimale à utiliser est la suivante (l'ordre des paramètres est important) :

`saveftp.py chemin hote`

* `chemin` : donne l'arborescence à sauvegarder. Si elle contient des espaces, il faudra l'entourer avec des doubles quotes. 
* `hote[:port]` : une adresse IP ou un nom pouvant être résolu comme telle. Si le port n'est pas spécifié, c'est celui par défaut pour les transferts FTP qui sera utilisé (port 21).

```
saveftp.py /home/user localhost
saveftp.py d:/developpement ftp.domaine.com
saveftp.py "c:/Program Files" 192.168.1.1:4242
```

### Les options

* `-u` ou `--user` : nom d'utilisateur pour le transfert FTP. Quand cette option n'est pas spécifiée, la connexion FTP se fait en anonyme.
* `-p` ou `--password` : mot de passe associé au nom d'utilisateur fourni. Si le user n'est pas spécifié, cette option est ignorée.

