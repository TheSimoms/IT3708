package ex1;

public class Config {
    public static final double STEP_SIZE = 0.1;

    public static final int NUMBER_OF_BOIDS = 50;

    public static final int WIDTH = 1024;
    public static final int HEIGHT = 576;

    public static final double BOID_RADIUS = 5.0;
    public static final double PREDATOR_RADIUS = 3.0 * BOID_RADIUS;
    public static final double NEIGHBOURHOOD_RADIUS = 15.0 * BOID_RADIUS;
    public static final double OBSTACLE_RADIUS = 5.0 * BOID_RADIUS;

    public static final double BOID_MAX_SPEED = 25.0;
    public static final double PREDATOR_MAX_SPEED = 1.25 * BOID_MAX_SPEED;

    public static final double AVOIDANCE_WEIGHT = 100.0;
    public static final double FLIGHT_WEIGHT = 75;
    public static final double CHASE_WEIGHT = 50.0;

    public static double ALIGNMENT_WEIGHT = 15.0;
    public static double SEPARATION_WEIGHT = 10.0;
    public static double COHESION_WEIGHT = 15.0;
}
