var subjectField = document.getElementById('id_subject');
var teacherField = document.getElementById('id_teacher');

function updateTeacherOptions() {
    var selectedSubject = subjectField.value;
    if (selectedSubject) {
        teacherField.disabled = true;
        while (teacherField.firstChild) {
            teacherField.removeChild(teacherField.firstChild);
        }
        fetch('/schedule/get_teachers/' + selectedSubject + '/')
            .then(response => response.json())
            .then(data => {
                data.forEach(teacher => {
                    var option = document.createElement('option');
                    option.value = teacher.id;
                    option.textContent = teacher.name;
                    teacherField.appendChild(option);
                });
                teacherField.disabled = false;
            })
            .catch(error => {
                console.error('Error while fetching teachers:', error);
                teacherField.disabled = false;
            });
    } else {
        console.log('Choose a subject before updating the teachers.');
    }
}

subjectField.addEventListener('change', updateTeacherOptions);
updateTeacherOptions();