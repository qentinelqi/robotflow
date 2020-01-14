*** Test Cases ***

action
    Log    action
    SetSuiteVariable      ${testvar}    1

start
    Log    Start

end
    Log    End
    ShouldBeEqual         ${testvar}    1
