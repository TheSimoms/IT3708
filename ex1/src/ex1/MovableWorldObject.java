package ex1;

import java.util.HashMap;

public abstract class MovableWorldObject extends WorldObject {
    private double vX, vY;
    private double maxSpeed;
    private double nextX, nextY;

    private boolean dead = false;

    private HashMap<MovableWorldObject, Double> distances = new HashMap<>();

    public abstract double[] calculateForces ();
    public abstract void clearNeighbours ();


    public double getvX () {
        return vX;
    }

    public void setvX (double vX) {
        this.vX = vX;
    }

    public double getvY () {
        return vY;
    }

    public void setvY (double vy) {
        this.vY = vy;
    }

    public double getNextX () {
        return nextX;
    }

    public void setNextX (double nextX) {
        this.nextX = nextX;
    }

    public double getNextY () {
        return nextY;
    }

    public void setNextY (double nextY) {
        this.nextY = nextY;
    }

    public double getMaxSpeed () {
        return maxSpeed;
    }

    public void setMaxSpeed (double maxSpeed) {
        this.maxSpeed = maxSpeed;
    }

    public boolean isDead () {
        return dead;
    }

    public void setDead (boolean dead) {
        this.dead = dead;
    }

    public HashMap<MovableWorldObject, Double> getDistances () {
        return distances;
    }

    public void setDistance (MovableWorldObject neighbour, double distance) {
        distances.put(neighbour, distance);
    }


    public MovableWorldObject (double x, double y, double radius, World world, double vX, double vY, double maxSpeed) {
        super(x, y, radius, world);

        this.vX = vX;
        this.vY = vY;

        this.maxSpeed = maxSpeed;

        this.nextX = x;
        this.nextY = y;
    }


    public double[] getVelocity () {
        return new double[] {vX, vY};
    }

    public double[] getNormalizedVelocity () {
        return Maths.normalizeVector(getVelocity());
    }

    public double getSpeed () {
        return Maths.vectorSize(getVelocity());
    }

    public void limitVelocity () {
        if (getSpeed() > maxSpeed) {
            double[] normalizedVelocity = getNormalizedVelocity();

            vX = maxSpeed * normalizedVelocity[0];
            vY = maxSpeed * normalizedVelocity[1];
        }
    }

    public void updateNextPosition () {
        double stepSize = Config.STEP_SIZE;

        nextX = (getX() + (stepSize * vX) + getWorld().getWidth()) % getWorld().getWidth();
        nextY = (getY() + (stepSize * vY) + getWorld().getHeight()) % getWorld().getHeight();
    }

    public void performMove () {
        if (!dead) {
            setX(nextX);
            setY(nextY);
        }
    }

    public void die () {
        dead = true;
    }

    public void updateVelocity () {
        if (isDead()) {
            return;
        }

        double[] forces = calculateForces();

        setvX(vX + forces[0]);
        setvY(vY + forces[1]);
    }

    public boolean isHittingObject (WorldObject object) {
        return shortestDistanceToObject(object) <= 0.0;
    }

    public boolean canSeeObject (WorldObject neighbour) {
        return shortestDistanceToObject(neighbour) + getRadius() < Config.NEIGHBOURHOOD_RADIUS;
    }
}
