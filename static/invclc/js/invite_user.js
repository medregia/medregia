document.addEventListener("DOMContentLoaded", () => {
    const selectElement = document.getElementById("id_storetype");
    const otherTypeElement = document.getElementById("id_other_value");
    const labelOtherElement = document.querySelector(".label-other");
  
    // Hide the elements initially
    otherTypeElement.style.display = "none";
    labelOtherElement.style.display = "none";
  
    selectElement.addEventListener("change", function () {
      if (this.value === "others") {
        // Show the elements when 'Others' is selected
        otherTypeElement.style.display = "block";
        labelOtherElement.style.display = "block";
  
        // Make the select field read-only
      //   selectElement.disabled = true;
      } else {
        // Hide the elements for any other selection
        otherTypeElement.style.display = "none";
        labelOtherElement.style.display = "none";
  
        // Enable the select field
      //   selectElement.disabled = false;
      }
    });
  
  });