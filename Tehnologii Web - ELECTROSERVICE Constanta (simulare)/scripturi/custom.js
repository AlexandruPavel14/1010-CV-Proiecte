$(window).on('load', function() {
    // Local Storage theme variable presenc check
    const currentThemeColor = localStorage.getItem('theme-color');

    if(currentThemeColor){
        // add class to body
        $('body').addClass(currentThemeColor);
        if(currentThemeColor == 'theme-dark'){
            $('.theme-switcher').prop('checked', true);
            $('.theme-switcher-label').addClass('active');
        } else{
            // continue with default theme
        }
    }
    // switch theme
    $('.theme-switcher-label').on('change', switchColorTheme);
});

function switchColorTheme(e){
    // console.log.(e.target.checked)
    $(this).toggleClass('active');
    // remove previous classes
    removeThemeClasses();
    if(e.target.checked){
        // its a dark theme
        $('body').addClass('theme-dark');
        localStorage.setItem('theme-color', 'theme-dark');
        $('.theme-switcher').prop('checked', true);
    } else{
        // its a light theme
        $('body').addClass('theme-light');
        localStorage.setItem('theme-color', 'theme-light');
        $('.theme-switcher').prop('checked', false);
    }

}

function removeThemeClasses(){
    //
    $('body').removeClass(function(index,cssName){
        return (cssName.match(/\btheme-\S+/g) || []).join(' ');
    })
}