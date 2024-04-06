jQuery(document).ready(function($) {
       $(document).ready(function(){
        $("#requiredControlsSwitch").on("change", function(e) {
          const isOn = e.currentTarget.checked;

          if (isOn) {
              $(".not_required").hide();
          } else {
              $(".not_required").show();
          }
        });
      });
});
