package ex1;

import java.util.HashMap;

public abstract class MovableWorldObject extends WorldObject {
    private double vX, vY;
    private double maxSpeed;
    private int nextX, nextY;

    private boolean dead = false;

    private HashMap<MovableWorldObject, Double> distances = new HashMap<>();

    public abstract double[] calculateForces ();


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

    public int getNextX () {
        return nextX;
    }

    public void setNextX (int nextX) {
        this.nextX = nextX;
    }

    public int getNextY () {
        return nextY;
    }

    public void setNextY (int nextY) {
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


    public MovableWorldObject (int x, int y, double radius, World world, double vX, double vY, double maxSpeed) {
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

        nextX = (getX() + (int)(stepSize * vX)) % getWorld().getWidth();
        nextY = (getY() + (int)(stepSize * vY)) % getWorld().getHeight();

        if (nextX < 0) {
            nextX += getWorld().getWidth();
        }

        if (nextY < 0) {
            nextY += getWorld().getHeight();
        }
    }

    public void performMove () {
        if (!dead) {
            setX(nextX);
            setY(nextY);
        }
    }

    public boolean die () {
        dead = true;

        return dead;
    }

    public void updateVelocity () {
        if (isDead()) {
            return;
        }

        double[] forces = calculateForces();

        setvX(vX + forces[0]);
        setvY(vY + forces[1]);
    }
}
