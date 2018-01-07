/**
 * Created by krzysiek on 07.01.18.
 */
function selectAll(source) {
    var checkboxes = document.getElementsByName('to_delete[]');
    for(var i in checkboxes)
        checkboxes[i].checked = source.checked;
}