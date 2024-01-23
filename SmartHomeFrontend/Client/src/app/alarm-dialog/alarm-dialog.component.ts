import { Component, OnInit } from '@angular/core';
import { ServiceService } from '../service.service';
import { MatDialog, MatDialogRef } from '@angular/material/dialog';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { DatePipe } from '@angular/common';

@Component({
  selector: 'app-alarm-dialog',
  templateUrl: './alarm-dialog.component.html',
  styleUrl: './alarm-dialog.component.css'
})
export class AlarmDialogComponent implements OnInit{

  datePipe = new DatePipe('en-US');

  alarmForm!: FormGroup;

  constructor(public dialogRef: MatDialogRef<AlarmDialogComponent>,private formBuilder: FormBuilder,
    private service: ServiceService,private dialog: MatDialog) {  
  }

  ngOnInit(): void {
    this.alarmForm = this.formBuilder.group({
      time:['',[Validators.required]],
    });
  }


  closeDialog(): void{
    this.dialogRef.close();
  }

  submit(): void{
    if (this.alarmForm.valid){
      //endpoint
      this.dialogRef.close();
    }

  }


}
