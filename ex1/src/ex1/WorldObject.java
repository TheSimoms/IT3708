package ex1;

/**
 * Created by user on 21.01.16.
 */
public abstract class WorldObject {
    private double x, y;
    private double radius;
    private World world;


    public double getX () {
        return x;
    }

    public void setX (double x) {
        this.x = x;
    }

    public double getY () {
        return y;
    }

    public void setY (double y) {
        this.y = y;
    }

    public double getRadius () {
        return radius;
    }

    public void setRadius (double radius) {
        this.radius = radius;
    }

    public World getWorld () {
        return world;
    }

    public void setWorld (World world) {
        this.world = world;
    }


    public WorldObject (double x, double y, double radius, World world) {
        this.x = x;
        this.y = y;
        this.radius = radius;
        this.world = world;
    }


    public double[] getPosition () {
        return new double[] {x, y};
    }

    public void setPosition (double[] position) {
        if (position.length == 2) {
            setX(position[0]);
            setY(position[1]);
        }
    }

    public double[] shortestDistanceVectorToPoint (double[] targetPoint) {
        double xDistance1 = targetPoint[0] - getX();
        double xDistance2 = -(Math.signum(xDistance1)) * (getWorld().getWidth() - Math.abs(xDistance1));

        double yDistance1 = targetPoint[1] - getY();
        double yDistance2 = -(Math.signum(yDistance1)) * (getWorld().getHeight() - Math.abs(yDistance1));

        double[] res = new double[2];

        if (Math.abs(xDistance1) <= Math.abs(xDistance2)) {
            res[0] = xDistance1;
        } else {
            res[0] = xDistance2;
        }

        if (Math.abs(yDistance1) <= Math.abs(yDistance2)) {
            res[1] = yDistance1;
        } else {
            res[1] = yDistance2;
        }

        return res;
    }

    public double shortestDistanceToPoint (double[] targetPoint) {
        return Maths.vectorSize(shortestDistanceVectorToPoint(targetPoint));
    }

    public double shortestDistanceToObject (WorldObject object) {
        return shortestDistanceToPoint(object.getPosition()) - getRadius() - object.getRadius();
    }

    public double distanceWeight (WorldObject object) {
        return Math.max(1.0 - ((this.shortestDistanceToObject(object) + getRadius()) / Config.NEIGHBOURHOOD_RADIUS), 0.0);
    }

    public boolean isOccupyingPosition (double[] position, double pointRadius) {
        return shortestDistanceToPoint(position) <= radius + pointRadius;
    }
}
