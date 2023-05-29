
package errores;

public class Errores {

   
    public static void main(String[] args) {
        double valorVerdadero = 0.51*100;
        double valorAproximado = 0.50*100;

        double errorAbsoluto = Math.abs(valorVerdadero - valorAproximado);
        double errorRelativo = (errorAbsoluto / valorVerdadero) * 100;

        System.out.println("El error absoluto es: " + errorAbsoluto);
        System.out.println("El error relativo es: " + errorRelativo + "%");
    }
}
    

