# Bots

Machine learning for robocode

## Setup

Note:
A copy of robocode is supplied with this repository

$PROJECT is the project folder

1. Install robocode `1.9.3.2`:
    
    - Open a terminal at $PROJECT/setup
    
    - Install robocode: run `./setup.sh`
      OR type `java -jar installers/robocode-1.9.3.2-setup.jar ./robocode-1.9.3.2`. 
      This installs robocode within the project folder. 
      If you install this way, you won't need to fix up any maven paths in pom.xml
    
    - OR `java -jar ./setup/robocode-1.8.3.0-setup.jar` then choose an installation folder,
      but keep a note of where robocode was installed, and you will need to adjust pom.xml

2. Install maven

    - https://maven.apache.org/install.html

3.a Build from command line
    
    `mvn clean install`

3.b Build from IDE

    - IntelliJ

        - Go to `Run` > `Edit Configurations...` > Click `+` (`Add New Configuration`) > Select `Application`
        - Configure with the below parameters:

            - `Name`: `Robocode`
            - `Main class`: `robocode.Robocode`
            - `VM options`: `-Xmx512M -Dsun.io.useCanonCaches=false -Ddebug=true`
            - `Working directory`: `/path/to/robocode` (from previous step)
            - `Use classpath of module`: `robocode`
                  
        - Alternatively, if you don't need the built-in robots (skip `Preferences` / `Development Options`)
            - `VM options`: `Xmx512M -Dsun.io.useCanonCaches=false -Ddebug=true -DNOSECURITY=true -DROBOTPATH=../target/classes`

    - Eclipse: [use these instructions](http://robowiki.net/wiki/Robocode/Running_from_Eclipse)

3. After setting up the IDE, robocode needs to know where the project robots are.

   - Run robocode
    `cd $PROJECT/robocode-1.9.3.2` then `./robocode.sh`.

   - Go to `Preferences` / `Development Options`, add path `$PROJECT/robocode/target/classes`

4. Train
    - Start the listener: `./python/listener.py`

    - Run the training: `./train.sh` or `slow-train.sh`
    
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
