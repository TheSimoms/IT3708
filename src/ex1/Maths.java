package ex1;

public class Maths {
    public static double vectorSize (double[] vector) {
        return Math.sqrt(Math.pow(vector[0], 2) + Math.pow(vector[1], 2));
    }
    public static double vectorSize (int[] vector) {
        return Math.sqrt(Math.pow(vector[0], 2) + Math.pow(vector[1], 2));
    }

    public static double distanceBetweenPoints (double[] vector0, double[] vector1) {
        return Math.sqrt(Math.pow(vector0[0] - vector1[0], 2) + Math.pow(vector0[1] - vector1[1], 2));
    }

    public static double distanceBetweenPoints (int[] vector0, int[] vector1) {
        return Math.sqrt(Math.pow(vector0[0] - vector1[0], 2) + Math.pow(vector0[1] - vector1[1], 2));
    }

    public static double angleBetweenVectors (double[] vector0, double[] vector1) {
        return Math.atan2(vector1[1], vector0[1]) - Math.atan2(vector1[0], vector0[0]);
    }

    public static double angleBetweenVectors (int[] vector0, int[] vector1) {
        return angleBetweenVectors(new double[]{(double)vector0[0], (double)vector0[1]}, new double[]{(double)vector1[0], (double)vector1[1]});
    }

    public static double[] normalizeVector (double[] vector) {
        double length = vectorSize(vector);

        if (length == 0.0) {
            return new double[] {0.0, 0.0};
        }

        return new double[] {vector[0]/length, vector[1]/length};
    }

    public static double[] normalizeVector (int[] vector) {
        return normalizeVector(new double[] {(double)vector[0], (double)vector[1]});
    }

    public static double[] scaleVectorToWeight (double[] vector, double weight) {
        return new double[] {vector[0] * weight, vector[1] * weight};
    }

    public static double direction (double[] vector) {
        return Math.atan2(vector[1], vector[0]);
    }

    public static boolean isPointInCircle (int[] point, int[] circleCenter, double radius) {
        return distanceBetweenPoints(point, circleCenter) <= radius;
    }

    public static int[] rotatePoint (int[] rotatePoint, int[] centerPoint, double radians) {
        int[] translated = new int[] {rotatePoint[0] - centerPoint[0], rotatePoint[1] - centerPoint[1]};
        double[] rotatedPoint = new double[] {translated[0] * Math.cos(radians) - translated[1] * Math.sin(radians), translated[0] * Math.sin(radians) + translated[1] * Math.cos(radians)};

        return new int[] {(int)(rotatedPoint[0] + centerPoint[0]), (int)(rotatedPoint[1] + centerPoint[1]) };
    }

    public static int[][] rotateObject (int[][] object, int[] centerPoint, double radians) {
        if (radians == 0.0) {
            return object;
        }

        int[][] res = new int[object.length][2];

        for (int i=0; i<object.length; i++) {
            res[i] = rotatePoint(object[i], centerPoint, radians);
        }

        return res;
    }
}
