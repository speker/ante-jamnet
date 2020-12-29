<div class="col-md-3">
<div class="card card-success">
<div class="card-header">
<h3 class="card-title">Modül : |module_id| - |module_name|</h3>
<div class="card-tools">
<button type="button" class="btn btn-tool" id="clear_alarm_|module_id|"><i class="fas fa-volume-off"></i>
</button>
</div>
</div>
<div class="card-body" style="display: block;">
<span><strong>Power</strong></span>
<div class="progress mb-3">
<div class="progress-bar bg-|module_progress|" role="progressbar" style="width: |module_state|%">
</div>
</div>
<div class="btn-group btn-group-toggle"  data-toggle="buttons">
<label class="btn btn-|module_high|">
<input type="radio" name="options" id="module_high_|module_id|" > High
</label>
<label class="btn btn-|module_middle|">
<input type="radio" name="options" id="module_middle_|module_id|" > Middle
</label>
<label class="btn btn-|module_low|">
<input type="radio" name="options" id="module_low_|module_id|"> Low
</label>
<label class="btn btn-|module_off| ">
<input type="radio" name="options" id="module_off_|module_id|"> Off
</label>
</div>
</div>
</div>
</div>