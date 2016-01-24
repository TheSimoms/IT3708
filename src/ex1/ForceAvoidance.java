package ex1;

public class ForceAvoidance extends Force {
    public ForceAvoidance (World world, double weight) {
        super(world, weight);
    }


    public double[] calculateForce (Boid boid) {
        double[] force = new double[] {0.0, 0.0};

        boid.setAvoiding(false);

        for (Obstacle obstacle : getWorld().getObstacles()) {
            double distance = boid.shortestDistanceToPoint(obstacle.getPosition());

            if (distance < Config.NEIGHBOURHOOD_RADIUS) {
                if (boid.isHittingObject(obstacle)) {
                    boolean dead = boid.die();

                    if (dead) {
                        return force;
                    }
                }

                boid.setAvoiding(true);

                double weight = 1 - (distance / Config.NEIGHBOURHOOD_RADIUS);
                double[] normalizedVelocity = boid.getNormalizedVelocity();
                int[] nextPosition = new int[] {boid.getX() + (int)(distance * normalizedVelocity[0]), boid.getY() + (int)(distance * normalizedVelocity[1])};

                double angle = Maths.angleBetweenVectors(boid.shortestDistanceVectorToPoint(obstacle.getPosition()), boid.shortestDistanceVectorToPoint(nextPosition));

                if (angle < 0.0) {
                    weight *= -1;
                }

                force[0] += -normalizedVelocity[1] * weight;
                force[1] += normalizedVelocity[0] * weight;
            }
        }

        return force;
    }
}
