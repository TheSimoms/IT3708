package ex1;

public class ForceAvoidance extends Force {
    public ForceAvoidance (World world, double weight) {
        super(world, weight);
    }


    public double[] calculateForce (Boid boid) {
        double[] force = new double[] {0.0, 0.0};

        boid.setAvoiding(false);

        for (Obstacle obstacle : getWorld().getObstacles()) {
            if (boid.canSeeObject(obstacle)) {
                double distance = boid.shortestDistanceToObject(obstacle);
                double[] normalizedVelocity = boid.getNormalizedVelocity();

                boolean isGoingToHit = false;

                for (double i = 0.5; i < (int)distance * 2.0; i += 0.5) {
                    double[] nextPosition = new double[] {boid.getX() + i * normalizedVelocity[0], boid.getY() + i * normalizedVelocity[1]};

                    if (obstacle.isOccupyingPosition(nextPosition, boid.getRadius() + 2.0)) {
                        isGoingToHit = true;

                        break;
                    }
                }

                if (isGoingToHit) {
                    boid.setAvoiding(true);

                    double weight = boid.distanceWeight(obstacle);
                    double[] nextPosition = new double[]{boid.getX() + (distance * normalizedVelocity[0]), boid.getY() + (distance * normalizedVelocity[1])};

                    double angle = Maths.angleBetweenVectors(boid.shortestDistanceVectorToPoint(obstacle.getPosition()), boid.shortestDistanceVectorToPoint(nextPosition));

                    if (angle < 0.0) {
                        weight *= -1;
                    }

                    force[0] += -normalizedVelocity[1] * weight;
                    force[1] += normalizedVelocity[0] * weight;
                }
            }
        }

        return force;
    }
}
