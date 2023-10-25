function writeToLog(app, text)
%get current datetime for logs
t = now;
d = string(datetime(t,'ConvertFrom','datenum'));
test = string(app.LogsTextArea.Value);
newText = d + ": " + text; %create new text row
app.LogsTextArea.Value = vertcat(test, newText); %adds text row to text log window
scroll(app.LogsTextArea, 'bottom'); %scrolls log window to bottom
end