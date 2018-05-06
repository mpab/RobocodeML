@echo off

set ROBOCODE=robocode-1.9.3.2
set CLSPTH="..\%ROBOCODE%\libs\*;..\java\target\lib\*"

echo %ROBOCODE%
echo %CLSPTH%

if "x%1" == "x" (
	echo "ERROR: no battle file specified, usage: %0 xxx.battle gui/headless"
	goto :eof
)

if not exist %1 (
    echo "ERROR: battle file: $1 not found"
    echo "from the ..\battles directory, you can select one of:"
    dir ..\battles\
	goto :eof
)

if "x%2" == "x" (
  echo "no gui option specified, running headless"
  java -Xmx512M ^
    -Dsun.io.useCanonCaches=false ^
    -Ddebug=true ^
    -DNOSECURITY=true ^
    -DROBOTPATH=..\%ROBOCODE%\robots ^
    -cp %CLSPTH% robocode.Robocode ^
    -battle %1 ^
    -nosound ^
    -nodisplay ^
    -tps 1000
    goto :eof
)

if "x%2" == "xgui" (
    echo "gui option specified, running with gui"
    java -Xmx512M ^
      -Dsun.io.useCanonCaches=false ^
      -Ddebug=true ^
      -DNOSECURITY=true ^
      -DROBOTPATH=..\%ROBOCODE%\robots ^
      -cp %CLSPTH% robocode.Robocode ^
      -battle %1 ^
      -tps 100
    goto :eof
)

echo "ERROR: invalid option specified, usage: %0 xxx.battle gui"
