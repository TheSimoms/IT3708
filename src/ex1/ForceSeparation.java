package ex1;

public class ForceSeparation extends Force {
    public ForceSeparation (World world, double weight) {
        super(world, weight);
    }


    public double[] calculateForce (Boid boid) {
        double[] force = new double[] {0.0, 0.0};

        if (boid.getVisibleNeighbours().size() == 0) {
            return force;
        }

        for (Boid neighbour : boid.getVisibleNeighbours()) {
            double weight = 1 - (boid.getDistanceToObject(neighbour) / Config.NEIGHBOURHOOD_RADIUS);
            double[] distanceVector = Maths.normalizeVector(boid.shortestDistanceVectorToPoint(neighbour.getPosition()));

            force[0] -= distanceVector[0] * weight;
            force[1] -= distanceVector[1] * weight;
        }

        return force;
    }
}
