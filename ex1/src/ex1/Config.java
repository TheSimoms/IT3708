package ex1;

public class Config {
    public static final double STEP_SIZE = 0.1;
    public static final boolean DEBUG = false;

    public static final int NUMBER_OF_BOIDS = 200;

    public static final int WIDTH = 1600;
    public static final int HEIGHT = 800;

    public static final double BOID_RADIUS = 7.5;
    public static final double PREDATOR_RADIUS = 3.0 * BOID_RADIUS;
    public static final double NEIGHBOURHOOD_RADIUS = 10.0 * BOID_RADIUS;
    public static final double OBSTACLE_RADIUS = 5.0 * BOID_RADIUS;

    public static final double BOID_MAX_SPEED = 25;
    public static final double PREDATOR_MAX_SPEED = 2.0 * BOID_MAX_SPEED;

    public static final double AVOIDANCE_WEIGHT = 200.0;
    public static final double FLIGHT_WEIGHT = 100.0;
    public static final double CHASE_WEIGHT = 50.0;

    public static final double FORCE_MAX_WEIGHT = 20.0;

    public static double ALIGNMENT_WEIGHT = 0.5 * FORCE_MAX_WEIGHT;
    public static double SEPARATION_WEIGHT = 0.75 * FORCE_MAX_WEIGHT;
    public static double COHESION_WEIGHT = 0.75 * FORCE_MAX_WEIGHT;
}
