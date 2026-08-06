# 🚀 GUIDE DU PILOTE (Niveau 1)

Bienvenue dans l'OASIS ! Avant que le casque **Meta Quest 3S** n'arrive, tu as déjà une mission très importante.
Ton papa (le Navigateur) a préparé le code de base, mais c'est à toi (le Pilote) de tester le jeu sur l'ordinateur !

## 🕹️ Ta Mission du Jour : Tester la Clé de Cuivre sur PC !

Même sans casque VR, tu peux te déplacer dans le jeu grâce au "Mode Clavier" que nous venons d'ajouter.

### Comment jouer dans Godot :
1. Demande à ton papa d'ouvrir le logiciel **Godot Engine 4** et d'ouvrir le `Projet OASIS`.
2. En haut à droite, clique sur le bouton **Play (F5)** (ou le petit triangle ⏯️).
3. Le HUB Central va s'ouvrir.
4. Utilise les touches de ton clavier pour te déplacer comme dans un jeu PC :
   - **W / Z** : Avancer
   - **S** : Reculer
   - **A / Q** : Gauche
   - **D** : Droite

### Ce que tu dois observer :
- Avance vers le portail bleu fluo (Portail de la Clé de Cuivre).
- Quand tu le touches, tu vas être téléporté dans le mini-jeu de la **Clé de Cuivre** !
- Essaie d'attraper la Clé flottante (le bloc orange lumineux).
- Regarde le score changer à l'écran !

## 🛠️ Le Code à comprendre (GDScript)
Regarde le fichier `scripts/key_copper/copper_key_level.gd` avec ton papa. Tu vas y voir ceci :

```gdscript
func add_points(amount: int) -> void:
	current_score += amount
	update_score_ui()
	if current_score >= 100 and not key_unlocked:
		unlock_copper_key()
```

**Question pour toi :** Si tu veux que le jeu demande **500 points** au lieu de 100 pour gagner la clé, quel chiffre dois-tu changer dans ce code ? Essaie de le changer avec ton papa et de relancer le jeu !
