package Common;

import org.json.JSONObject;

public class Observation {

    // metadata
    int round;
    int num_rounds;
    public int frame;
    // features
    public int action;
    public double x;
    public double y;
    public double heading;
    // NOTE
    // some features (named scanned_*) are only valid if the robot was scanned
    // if this flag is true, the features are valid
    public boolean scanned;
    public double scanned_enemy_distance;
    public double scanned_enemy_bearing;
    public double scanned_enemy_x;
    public double scanned_enemy_y;

    // events
    public int enemy_collisions;
    public int wall_collisions;
    public int shell_hits;
    public int shell_wounds;
    public int shell_misses;
    public int shell_intercepts;

    public int handshake;

    public Observation(int round, int num_rounds, int frame, int action) {
        this.round = round;
        this.num_rounds = num_rounds;
        this.frame = frame;
        this.action = action;
    }

    public JSONObject toJson() {

        JSONObject jsn = new JSONObject();
        // metadata
        jsn.put("round", round);
        jsn.put("num_rounds", num_rounds);
        jsn.put("frame", frame);
        // features
        jsn.put("action", action);
        jsn.put("x", x);
        jsn.put("y", y);
        jsn.put("heading", heading);
        jsn.put("scanned", scanned);
        jsn.put("scanned_enemy_distance", scanned_enemy_distance);
        jsn.put("scanned_enemy_bearing", scanned_enemy_bearing);
        jsn.put("scanned_enemy_x", scanned_enemy_x);
        jsn.put("scanned_enemy_y", scanned_enemy_y);
        // events
        jsn.put("enemy_collisions", enemy_collisions);
        jsn.put("wall_collisions", wall_collisions);
        jsn.put("shell_hits", shell_hits);
        jsn.put("shell_wounds", shell_wounds);
        jsn.put("shell_misses", shell_misses);
        jsn.put("shell_intercepts", shell_intercepts);

        jsn.put("handshake", handshake);

        return jsn;
    }
}
