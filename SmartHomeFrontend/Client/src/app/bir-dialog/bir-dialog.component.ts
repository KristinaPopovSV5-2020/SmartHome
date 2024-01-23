import { Component } from '@angular/core';
import { MatDialog, MatDialogRef } from '@angular/material/dialog';
import { ServiceService } from '../service.service';
import { FormBuilder } from '@angular/forms';

@Component({
  selector: 'app-bir-dialog',
  templateUrl: './bir-dialog.component.html',
  styleUrl: './bir-dialog.component.css'
})
export class BirDialogComponent {

  code = "";

  constructor(public dialogRef: MatDialogRef<BirDialogComponent>,private formBuilder: FormBuilder,
    private service: ServiceService,private dialog: MatDialog) {  
  }
  buttons = [
    { label: '1', command: 'button_1', color: '#3498db' },
    { label: '2', command: 'button_2', color: '#3498db'},
    { label: '3', command: 'button_3', color: '#3498db' },
    { label: '4', command: 'button_4', color: '#3498db' },
    { label: '5', command: 'button_5', color: '#3498db' },
    { label: '6', command: 'button_6' , color: '#3498db'},
    { label: '7', command: 'button_7', color: '#3498db' },
    { label: '8', command: 'button_8' , color: '#3498db'},
    { label: '9', command: 'button_9' , color: '#3498db'},
    { label: '*', command: 'button_*' , color: '#FF0000'},
    { label: '0', command: 'button_0' , color: '#3498db'},
    { label: '#', command: 'button_#' , color: '#FF0000'},
  ];

  onButtonClick(button: any): void {
    this.code = button.label
    this.service.birChangeDevice(this.code).subscribe({next:
      (response)=>{
        this.dialogRef.close(); 
      }, error: (error)=> {
        console.error(error)
      }})

  }



  closeDialog(): void{
    this.dialogRef.close();

  }

}
