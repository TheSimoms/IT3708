package ex1;

public class Maths {
    public static double vectorSize (double[] vector) {
        return Math.sqrt(Math.pow(vector[0], 2) + Math.pow(vector[1], 2));
    }

    public static double distanceBetweenPoints (double[] vector0, double[] vector1) {
        return Math.sqrt(Math.pow(vector0[0] - vector1[0], 2) + Math.pow(vector0[1] - vector1[1], 2));
    }

    public static double angleBetweenVectors (double[] vector0, double[] vector1) {
        return Math.atan2(vector1[1], vector1[0]) - Math.atan2(vector0[1], vector0[0]);
    }

    public static double[] addVectors (double[] vector0, double[] vector1) {
        return new double[] {
                vector0[0] + vector1[0],
                vector0[1] + vector1[1]
        };
    }

    public static double[] multiplyVectors (double[] vector0, double[] vector1) {
        return new double[] {
                vector0[0] * vector1[0],
                vector0[1] * vector1[1]
        };
    }

    public static double[] scaleVector (double[] vector, double weight) {
        return new double[] {vector[0] * weight, vector[1] * weight};
    }

    public static double[] normalizeVector (double[] vector) {
        double length = vectorSize(vector);

        if (length == 0.0) {
            return new double[] {0.0, 0.0};
        }

        return new double[] {vector[0] / length, vector[1] / length};
    }

    public static double vectorDirection (double[] vector) {
        return Math.atan2(vector[1], vector[0]);
    }
}
