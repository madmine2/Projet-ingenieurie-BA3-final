Pyraminx machine 


Le dossier src contient le code du pyraminx-solver de nilaymaj (https://github.com/nilaymaj/pyraminx-solver).
main_pyraminx.py est un fichier pour utiliser ce code, il s'agit d'une version modifiée du main du pyraminx-solver. 

main_link.py est le fichier principal à lancer, il fait le lien entre le pyraminx-solver et les autres parties.

acquisition.py s'occupe du contrôle des caméra et de la reconnaissance des couleurs.

conversion.py fait la conversion des mouvements fournis par le pyraminx-solver (qui sont des lettres)
en chiffres et permet de plus facilement controller  les moteurs manuellement. Il envoie les infos à control_motor.py

control_motor.py permet de controller les différents moteurs à partir de la raspberry pi