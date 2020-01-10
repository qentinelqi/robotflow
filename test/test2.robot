*** Test Cases ***
start
    Log    Start
    SetSuiteVariable      ${count}    0
    ${count}=             ConvertToInteger    ${count}

action
    Log    action

checknumber
    SetSuiteVariable      ${OUTPUT}    false
    Log                   Checknumber count: ${count}
    # ${OUTPUT}=            Set Variable If       ${count} == 2   true    false
    RunKeywordIf          ${count} == 2    SetSuiteVariable    ${OUTPUT}    true

increment
    SetSuiteVariable      ${count}
    ${count}=             Evaluate    ${count} + 1
    Log                   Increment count: ${count}
    SetSuiteVariable      ${count}



end
    Log                       End
    ShouldBeEqualAsStrings    ${count}    2