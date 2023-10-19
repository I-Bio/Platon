let variantsContainer = document.querySelector(".cont-quest");
let iterator = 0;

document.querySelector("form").addEventListener('formdata', (e) => {

    const formData = e.formData; 
    
    let answerCheckboxes = document.getElementsByName("answerCheckbox");

    answerCheckboxes.forEach(el => {
        formData.append('option_answer[]', el.checked ? 1 : 0);
    })

    
});

window.onload = function (){

    updateLabelInputLinks();
    updateAnswerOptions();
    validateQuestion();

    let answerCheckboxes = document.getElementsByName("answerCheckbox");

    answerCheckboxes.forEach((el) => {
        if (el.hasAttribute("checked")) 
        {   
            el.checked = true;
        }
    });
}

$("#selectAllButton").click(
    function () {
        let selectCheckboxes = document.getElementsByName("selectCheckbox");
        let selectAllButton = document.getElementById("selectAllButton");

        let selected = false;

        if (selectAllButton.textContent == "Выбрать всё")
        {
            selected = true;
            setSelectAllButtonState(true);
        }
        else
        {
            setSelectAllButtonState(false);
        }

        selectCheckboxes.forEach((el) => {
            el.checked = selected;
        })
    }
);

function setSelectAllButtonState(state) 
{
    if (state) 
    {
        selectAllButton.textContent = "Снять выделение";
    }
    else 
    {
        selectAllButton.textContent = "Выбрать всё";
    }
}

function updateSelectAllButton() 
{
    let selectCheckboxes = document.getElementsByName("selectCheckbox");

    for (let i = 0; i < selectCheckboxes.length; i++) 
    {
        if (selectCheckboxes[i].checked) 
        {
            setSelectAllButtonState(true);
            return;
        }
    }

    setSelectAllButtonState(false);
}

$("#addQuestionButton").click(
    function () {
        const template = document.querySelector("#answerOptionTemplate");
        let clone = template.content.cloneNode(true);
        let options = document.querySelector(".cont-quest");
        
        options.append(clone);

        updateLabelInputLinks();
        validateQuestion();

        updateAnswerOptions();
    }
);

$("#deleteSelectedButton").click(
    function (){
        let allSelectedInputs = document.getElementsByName("selectCheckbox");
        
        for (let i = 0; i < allSelectedInputs.length;) 
        {
            if (allSelectedInputs[i].checked) 
            {
                allSelectedInputs[i].parentNode.parentNode.remove();
            }
            else 
            {
                i++;
            }
        }

        updateLabelInputLinks();
        updateSelectAllButton();
        validateQuestion();
    }
);

function updateAnswerOptions() 
{
    const questionType = document.getElementById("questionType");
    let allAnswCheckBox = document.getElementsByName("answerCheckbox");

    if (questionType.value == 0)
    {
        allAnswCheckBox.forEach((el) => {
            el.onclick = function ()
            {
                resetAnswerCheckbox();
                this.checked = true;
            }
        });
    }
    else if (questionType.value == 1)
    {
        allAnswCheckBox.forEach((el) => {
            el.onclick = function () {}
        });
    }
}

function answerOneOption(element) 
{
    resetAnswerCheckbox();
    element.checked = true;
};

function resetAnswerCheckbox() 
{
    let allAnswCheckBox = document.getElementsByName("answerCheckbox");
    
    allAnswCheckBox.forEach((el) => {
        el.checked = false;
    });
};

function deleteAnswer(element) {
    element.parentNode.parentNode.remove();

    updateLabelInputLinks();
    updateSelectAllButton();
    validateQuestion();
};


function updateLabelInputLinks() 
{
    let selectInputs = document.getElementsByName("selectCheckbox");
    
    selectInputs.forEach((el) => {
        el.id = `selectCheckbox${iterator}`;
        el.nextSibling.nextSibling.htmlFor = `selectCheckbox${iterator}`;

        iterator += 1;
    });

    let answerInputs = document.getElementsByName("answerCheckbox");
    
    answerInputs.forEach((el) => {
        el.id = `selectCheckbox${iterator}`;
        el.nextSibling.nextSibling.htmlFor = `selectCheckbox${iterator}`;

        iterator += 1;
    });
}

function validateQuestion(){
    const submitButton = document.getElementById("submitButton");

    if (variantsContainer.childElementCount < 2)
    {
        document.getElementById("warning").textContent = "Необходимо минимум два варианта ответа";
        submitButton.setAttribute("disabled","");
    }
    else 
    {
        document.getElementById("warning").textContent = "";
        submitButton.removeAttribute("disabled");
    }
}