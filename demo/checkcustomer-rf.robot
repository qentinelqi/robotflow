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
Check CustomerIds
    Log    Start
    RemoveFile                   ${output_xlsx}
    OpenBrowser                  ${location}                ${BROWSER}
    WaitUntilPageContains        Check CustomerId

    # Read input
    OpenExcelDocument            filename=${input_xlsx}     doc_id=input
    ${col}=                      Read Excel Column          col_num=1
    Remove From List             ${col}                     0
    CloseAllExcelDocuments

    # Create output Excel
    CreateExcelDocument          output
    WriteExcelCell               1                          1     CustomerId
    WriteExcelCell               1                          2     Status
    ${output_row}                SetVariable                1

    # Main loop that checks all customerIds
    FOR                          ${CustomerId}    IN   @{col}
        # Open page and handle errors
        GoTo                     ${location}
        ${status}   ${message}=  RunKeywordAndIgnoreError   WaitUntilPageContains    Customer checker      1s
        RunKeywordIf             "${status}" == "FAIL"      WriteExcelCell           ${output_row}         2    ERROR
        RunKeywordIf             "${status}" == "FAIL"      Save Excel Document      ${output_xlsx}
        ContinueForLoopIf        "${status}" == "FAIL"

        InputText                customerid                 ${CustomerId}
        ${output_row}=           Evaluate                   ${output_row} + 1
        WriteExcelCell           ${output_row}              1     ${CustomerId}
        ClickButton              saveForm

        # Handle errors in page
        ${status}   ${message}=  RunKeywordAndIgnoreError   WaitUntilPageContains    CustomerId result     1s
        RunKeywordIf             "${status}" == "FAIL"      WriteExcelCell           ${output_row}         2    ERROR
        RunKeywordIf             "${status}" == "FAIL"      Save Excel Document      ${output_xlsx}
        ContinueForLoopIf        "${status}" == "FAIL"
        ${result}=               GetText                    result
        WriteExcelCell           ${output_row}              2                        ${result}
        Save Excel Document      ${output_xlsx}
    END
    Save Excel Document          ${output_xlsx}
    CloseAllExcelDocuments

    # Check that expected data is in output.xlsx
    OpenExcelDocument            filename=${output_xlsx}    doc_id=output
    ${targetlist1}=              CreateList                 CustomerId  346  432  3445  000  732  834
    ${col1}=                     ReadExcelColumn            1
    ListsShouldBeEqual           ${targetlist1}             ${col1}
    ${targetlist2}=              CreateList                 Status  Unknown customer  Customer is expired  Invalid CustomerId  ERROR  Customer is valid  Customer is valid
    ${col2}=                     ReadExcelColumn            2
    ListsShouldBeEqual           ${targetlist2}             ${col2}
    CloseAllExcelDocuments
