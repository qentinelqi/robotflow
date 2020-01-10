*** Settings ***
Library                   Collections
Library                   OperatingSystem
Library                   SeleniumLibrary
Library                   ExcelLibrary.py
Suite Teardown            Close All Browsers

*** Variables ***
${BROWSER}                gc
${location}               http://localhost:8080/
${input_xlsx}             input.xlsx
${output_xlsx}            output.xlsx

*** Tasks ***
Start
    Log                      Start
    OpenBrowser              ${location}                ${BROWSER}
    WaitUntilPageContains    Check CustomerId
    RemoveFile               ${output_xlsx}

Load data
    # Load input date
    OpenExcelDocument         filename=${input_xlsx}    doc_id=input
    ${col}=                   ReadExcelColumn           col_num=1
    RemoveFromList            ${col}                    0
    SetSuiteVariable          ${col}
    CloseAllExcelDocuments

    # Create outout Excel
    CreateExcelDocument       output
    WriteExcelCell            1                         1               CustomerId
    WriteExcelCell            1                         2               Status
    SaveExcelDocument         ${output_xlsx}
    SetSuiteVariable          ${output_row}             1

CustomerIds left
    SetSuiteVariable          ${OUTPUT}                 true
    ${count}=                 Get Length                ${col}
    ${OUTPUT}=                Set Variable If           ${count} == 0   false     true

Check CustomerId
    ${output_row}=            Evaluate                  ${output_row} + 1
    SetSuiteVariable          ${output_row}
    ${CustomerId}=            Remove From List          ${col}          0
    WriteExcelCell            ${output_row}             1               ${CustomerId}

    GoTo                      ${location}
    WaitUntilPageContains     Customer checker          1s
    InputText                 customerid                ${CustomerId}
    ClickButton               saveForm
    WaitUntilPageContains     CustomerId result         1s
    ${result}=                GetText                   result

    LogToConsole              ${result}
    WriteExcelCell            ${output_row}             2               ${result}
    SaveExcelDocument         ${output_xlsx}
    [Teardown]                CheckCustomerTeardown

Close Documents
    CloseAllExcelDocuments

End
    [tags]    dev
    Log                       End
    # Check that expected data is in output.xlsx
    OpenExcelDocument         filename=output.xlsx      doc_id=output
    ${targetlist1}=           CreateList                CustomerId  346  432  3445  000  732  834
    ${col1}=                  ReadExcelColumn           1
    ListsShouldBeEqual        ${targetlist1}            ${col1}
    ${targetlist2}=           CreateList                Status  Unknown customer  Customer is expired  Invalid CustomerId  ERROR  Customer is valid  Customer is valid
    ${col2}=                  ReadExcelColumn           2
    ListsShouldBeEqual        ${targetlist2}            ${col2}
    CloseAllExcelDocuments

*** Keywords ***
CheckCustomerTeardown
    RunKeywordIfTestFailed    WriteExcelCell            ${output_row}    2    ERROR
    SaveExcelDocument         ${output_xlsx}