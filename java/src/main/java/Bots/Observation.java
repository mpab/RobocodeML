package Bots;

import org.json.JSONObject;

public class Observation {

    // metadata
    int round;
    int num_rounds;
    int frame;
    // features
    int action;
    double x;
    double y;
    double heading;
    // NOTE
    // some features (named scanned_*) are only valid if the robot was scanned
    // if this flag is true, the features are valid
    boolean scanned;
    double scanned_enemy_distance;
    double scanned_enemy_bearing;

    // events
    int enemy_collisions;
    int wall_collisions;
    int shell_hits;
    int shell_wounds;
    int shell_misses;
    int shell_intercepts;

    public Observation(int round, int num_rounds, int frame, int action, double x, double y, double heading) {
        this.round = round;
        this.num_rounds = num_rounds;
        this.frame = frame;
        this.action = action;
        this.x = x;
        this.y = y;
        this.heading = heading;
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
        // events
        jsn.put("enemy_collisions", enemy_collisions);
        jsn.put("wall_collisions", wall_collisions);
        jsn.put("shell_hits", shell_hits);
        jsn.put("shell_wounds", shell_wounds);
        jsn.put("shell_misses", shell_misses);
        jsn.put("shell_intercepts", shell_intercepts);

        return jsn;
    }
}
