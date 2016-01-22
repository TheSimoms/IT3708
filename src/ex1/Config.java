package ex1;

public class Config {
    public static double STEP_SIZE = 0.1;

    public static int NUMBER_OF_BOIDS = 200;

    public static double BOID_RADIUS = 5;
    public static double PREDATOR_RADIUS = 3 * BOID_RADIUS;
    public static double NEIGHBOURHOOD_RADIUS = 10 * BOID_RADIUS;
    public static double OBSTACLE_RADIUS = 5 * BOID_RADIUS;

    public static double BOID_MAX_SPEED = 50.0;
    public static double PREDATOR_MAX_SPEED = 1.25 * BOID_MAX_SPEED;

    public static double AVOIDANCE_WEIGHT = 1.0;
    public static double FLIGHT_WEIGHT = 0.75;
    public static double CHASE_WEIGHT = 0.5;
}
