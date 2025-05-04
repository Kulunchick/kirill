// Скрипт для встановлення певних обмежень при введенні значень у формі генерації завдань

document.addEventListener("DOMContentLoaded", function () {
    const jobsAmountMinInput = document.querySelector('input[name="jobs_amount_min"]');
    const jobsAmountMaxInput = document.querySelector('input[name="jobs_amount_max"]');
    const jobsDurationMinInput = document.querySelector('input[name="jobs_duration_min"]');
    const jobsDurationMaxInput = document.querySelector('input[name="jobs_duration_max"]');

    function setInputConstraints(minInput, maxInput) {
        minInput.addEventListener("blur", () => {
            if (+maxInput.value && +minInput.value > +maxInput.value)
                minInput.value = +maxInput.value;
            if (+minInput.value)
                maxInput.min = +minInput.value;
        });

        maxInput.addEventListener("blur", () => {
            if (+minInput.value && +maxInput.value < +minInput.value)
                maxInput.value = +minInput.value;
            if (+minInput.value) {
                maxInput.min = +minInput.value;
                minInput.max = +maxInput.value;
            }
        });
    }

    function setMaxDurationConstraint(inputField) {
        inputField.addEventListener("blur", () => {
            if (+jobsDurationMinInput.value && +jobsAmountMaxInput.value) {
                jobsDurationMaxInput.min = +jobsDurationMinInput.value + +jobsAmountMaxInput.value - 1;
            }
            if (+jobsDurationMaxInput.value < +jobsDurationMinInput.value + +jobsAmountMaxInput.value - 1)
                jobsDurationMaxInput.value = +jobsDurationMinInput.value + +jobsAmountMaxInput.value - 1;
        });
    }

    setInputConstraints(jobsAmountMinInput, jobsAmountMaxInput);
    setInputConstraints(jobsDurationMinInput, jobsDurationMaxInput);
    setMaxDurationConstraint(jobsAmountMaxInput);
    setMaxDurationConstraint(jobsDurationMinInput);
    setMaxDurationConstraint(jobsDurationMaxInput);
});
