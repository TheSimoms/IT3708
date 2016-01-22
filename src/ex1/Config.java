package ex1;

public class Config {
    public static final double STEP_SIZE = 1;

    public static final int NUMBER_OF_BOIDS = 200;

    public static final int WIDTH = 1024;
    public static final int HEIGHT = 576;

    public static final double BOID_RADIUS = 5;
    public static final double PREDATOR_RADIUS = 3 * BOID_RADIUS;
    public static final double NEIGHBOURHOOD_RADIUS = 10 * BOID_RADIUS;
    public static final double OBSTACLE_RADIUS = 5 * BOID_RADIUS;

    public static final double BOID_MAX_SPEED = 50.0;
    public static final double PREDATOR_MAX_SPEED = 1.25 * BOID_MAX_SPEED;

    public static final double AVOIDANCE_WEIGHT = 1.0;
    public static final double FLIGHT_WEIGHT = 0.75;
    public static final double CHASE_WEIGHT = 0.5;

    public static double ALIGNMENT_WEIGHT = 1.0;
    public static double SEPARATION_WEIGHT = 1.0;
    public static double COHESION_WEIGHT = 1.0;
}
