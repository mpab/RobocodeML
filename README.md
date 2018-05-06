# Robocode ML

Machine learning for robocode

## Project Structure

```
$PROJECT
|-analysis/     # analytics data
|-battles/       # battle configurations
|-data/          # generated/reprocessed data from robocode
|-doc/           # project documentation
|-installers/    # 3rd-party installers
|-java/          # java source files
|-python/        # python source files (capture/training/analytics/ML)
|-scripts/       # shell scripts
|-README.md
```

## Setup

Note:
A copy of robocode is supplied with this repository

$PROJECT is the root of the project folder

1. Install robocode `1.9.3.2`:

    - Open a terminal at $PROJECT/scripts

    - Install robocode: run `./setup` (This installs robocode within the project folder, if you install like this, you won't need to fix up any maven paths in pom.xml)

2.a Install java dependencies

    - https://maven.apache.org/install.html

    - JDK 8

2.b Install python dependencies
    - python3
    - python3-venv
    - python3-pip
    - python3-tk

3.a Build from command line: `./build`

3.b Build from IDE

- IntelliJ (assuming the project root is ./java/)

- Open the ./java roject and make sure you import the pom.xml (you may get a warning about this)

    - Go to `Run` > `Edit Configurations...` > Click `+` (`Add New Configuration`) > Select `Application`

    - Configure with the below parameters:

        - `Name`: `random-vs-random.battle` (recommend one configuration per)

        - `Main class`: `robocode.Robocode`

        - IF you want to configure robocode to automatically find the project robots

            - `VM options`: `-Xmx512M -Dsun.io.useCanonCaches=false -Ddebug=true -DNOSECURITY=true -DROBOTPATH=../java/target/classes`

        - ELSE if you want to set the robots path from within robocode (see '4')

            - `VM options`: `--Xmx512M -Dsun.io.useCanonCaches=false -Ddebug=true`

        - Program arguments: `-battle ../battles/random-vs-random.battle`

        - `Working directory`: `/path/to/robocode` (from previous step)
              e.g. `$HOME/Projects/RobocodeML/robocode-1.9.3.2`

        - `Use classpath of module`: `RobocodeML`

    - You will then need to add the Robocode jars to your classpath, (how you do this depends on the version of IntelliJ)
    In IntelliJ, go to the `Project Settings/Project/Modules` proprties page
    Select the dependencies tab
    Add (click +) JARs or directories
    Select the libs folder in your Robocode installation - e.g. `$HOME/Projects/RobocodeML/robocode-1.9.3.2/libs`

    - Make sure you name this configuration (e.g.`random-vs-random.battle`) and click Apply or OK, otherwise you'll have to start again

    - Run or Debug

- Eclipse: [use these instructions](http://robowiki.net/wiki/Robocode/Running_from_Eclipse)


4. (Optional) After setting up the IDE, robocode needs to know where the project robots are.

   - Run robocode
    `cd $PROJECT/robocode-1.9.3.2` then `./robocode.sh`.

   - Go to `Preferences` / `Development Options`, add path `$PROJECT/robocode/target/classes`

5. Run from command line

    - Start the capture: (data is saved to ./data/)

        `./capture`

    - Run the Training bot vs the Random bot in Robocode:

        `./battle-test-random` (headless) or `./battle-test-random-gui`

## Notes

`java.io.FileNotFoundException: ... /org/json/JSONObject.class (No such file or directory)`

Ignore this: I suspect robocode's class loader logs this erroneously, but the json module works fine

## Resources

- [http://robocode.sourceforge.net/docs/robocode/](http://robocode.sourceforge.net/docs/robocode/)
- [http://robowiki.net/wiki/Talk:Wall_Avoidance](http://robowiki.net/wiki/Talk:Wall_Avoidance)
- [http://robowiki.net/wiki/Wall_Smoothing](http://robowiki.net/wiki/Wall_Smoothing)
- [http://robowiki.net/wiki/Wall_Smoothing/Implementations](http://robowiki.net/wiki/Wall_Smoothing/Implementations)
- [http://www.ibm.com/developerworks/library/j-robotips/index.html](http://www.ibm.com/developerworks/library/j-robotips/index.html)
  - [Anti-gravity movement](http://www.ibm.com/developerworks/library/j-antigrav/index.html)
  - [Predictive targeting](http://www.ibm.com/developerworks/library/j-pred-targeting/index.html)
  - [Tracking your opponents' movement](http://www.ibm.com/developerworks/java/library/j-movement/index.html)
  - [Circular targeting](http://www.ibm.com/developerworks/library/j-circular/index.html)
  - [Dodge bullets](http://www.ibm.com/developerworks/library/j-dodge/index.html)
  - [Tracking bullets](http://www.ibm.com/developerworks/library/j-tipbullet.html)
  - [Radar sweeps](http://www.ibm.com/developerworks/library/j-radar/index.html)
  - [Polymorphic enemy cache](http://www.ibm.com/developerworks/library/j-tippoly/)
  - [Robocode strategies](http://www.ibm.com/developerworks/library/j-tipstrats/index.html)
