package ex1;

public class ForceAlignment extends Force {
    public ForceAlignment (World world, double weight) {
        super(world, weight);
    }


    public double[] calculateForce (Boid boid) {
        double[] force = new double[] {0.0, 0.0};

        if (boid.getVisibleNeighbours().size() == 0) {
            return force;
        }

        for (Boid neighbour : boid.getVisibleNeighbours()) {
            double weight = boid.distanceWeight(neighbour);
            double[] neighbourVelocity = neighbour.getNormalizedVelocity();

            force[0] += neighbourVelocity[0] * weight;
            force[1] += neighbourVelocity[1] * weight;
        }

        return Maths.normalizeVector(force);
    }
}
