package ex1;

/**
 * Created by user on 21.01.16.
 */
public abstract class WorldObject {
    private int x, y;
    private int radius;
    private World world;


    public int getX () {
        return x;
    }

    public void setX (int x) {
        this.x = x;
    }

    public int getY () {
        return y;
    }

    public void setY (int y) {
        this.y = y;
    }

    public int getRadius () {
        return radius;
    }

    public void setRadius (int radius) {
        this.radius = radius;
    }

    public World getWorld () {
        return world;
    }

    public void setWorld (World world) {
        this.world = world;
    }


    public WorldObject (int x, int y, double radius, World world) {
        this.x = x;
        this.y = y;
        this.world = world;
    }


    public int[] getPosition () {
        return new int[] {x, y};
    }

    public void setPosition (int[] position) {
        if (position.length == 2) {
            setX(position[0]);
            setY(position[1]);
        }
    }

    public int[] shortestDistanceVectorToPoint (int[] targetPoint) {
        int xDistance1 = targetPoint[0] - getX();
        int xDistance2 = -(Integer.signum(xDistance1)) * (getWorld().getWidth() - Math.abs(xDistance1));

        int yDistance1 = targetPoint[1] - getY();
        int yDistance2 = -(Integer.signum(yDistance1)) * (getWorld().getHeight() - Math.abs(yDistance1));

        int[] res = new int[2];

        if (Math.abs(xDistance1) <= Math.abs(xDistance2)) {
            res[0] = xDistance1;
        } else {
            res[0] = xDistance2;
        }

        if (Math.abs(yDistance1) <= Math.abs(yDistance2)) {
            res[0] = yDistance1;
        } else {
            res[0] = yDistance2;
        }

        return res;
    }

    public double shortestDistanceToPoint (int[] targetPoint) {
        return Maths.vectorSize(shortestDistanceVectorToPoint(targetPoint));
    }

    public double getDistanceToObject (WorldObject object) {
        return shortestDistanceToPoint(object.getPosition());
    }

    public boolean isHittingObject (WorldObject object) {
        return getDistanceToObject(object) < radius + object.getRadius();
    }
}
