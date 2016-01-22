package ex1;

public class ForceFlight extends Force {
    public ForceFlight (World world, double weight) {
        super(world, weight);
    }


    public double[] calculateForce (Boid boid) {
        double[] force = new double[] {0.0, 0.0};

        boid.setFleeing(boid.getVisiblePredators().size() > 0);

        for (Predator predator : boid.getVisiblePredators()) {
            if (boid.isHittingObject(predator)) {
                boolean dead = boid.die();

                if (dead) {
                    return force;
                }
            }

            double weight = 1 - (boid.getDistances().get(predator) / Config.NEIGHBOURHOOD_RADIUS);
            int[] distanceVector = boid.shortestDistanceVectorToPoint(predator.getPosition());

            force[0] = distanceVector[0] * weight;
            force[1] = distanceVector[1] * weight;
        }

        return force;
    }
}
