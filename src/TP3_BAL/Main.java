package TP3_BAL;

public class Main {

	public static void main(String[] args) {

		Boite_aux_lettres boite_aux_lettres = new Boite_aux_lettres();

		Consommateur consommateur = new Consommateur();
		Producteur producteur = new Producteur();

		consommateur.boite_aux_lettres = boite_aux_lettres;
		producteur.boite_aux_lettres = boite_aux_lettres;
		producteur.lettre = "Bonjour";

		producteur.start();
		consommateur.start();



	}

}
