package ex1;

public abstract class Force {
    private World world;
    private double weight;

    public double getWeight () {
        return weight;
    }

    public void setWeight (double weight) {
        this.weight = weight;
    }

    public World getWorld () {
        return world;
    }

    public void setWorld (World world) {
        this.world = world;
    }


    public Force (World world, double weight) {
        this.world = world;
        this.weight = weight;
    }


    public abstract double[] calculateForce(Boid boid);
}
