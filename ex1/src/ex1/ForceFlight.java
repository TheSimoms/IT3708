package ex1;

public class ForceFlight extends Force {
    public ForceFlight (World world, double weight) {
        super(world, weight);
    }


    public double[] calculateForce (Boid boid) {
        double[] force = new double[] {0.0, 0.0};

        boid.setFleeing(boid.getVisiblePredators().size() > 0);

        for (Predator predator : boid.getVisiblePredators()) {
            double weight = boid.distanceWeight(predator);
            double[] distanceVector = boid.shortestDistanceVectorToPoint(predator.getPosition());

            force[0] -= distanceVector[0] * weight;
            force[1] -= distanceVector[1] * weight;
        }

        return force;
    }
}
