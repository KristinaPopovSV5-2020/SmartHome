import { Component } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { MatDialog, MatDialogRef } from '@angular/material/dialog';
import { ServiceService } from '../service.service';

@Component({
  selector: 'app-dms-dialog',
  templateUrl: './dms-dialog.component.html',
  styleUrl: './dms-dialog.component.css'
})
export class DmsDialogComponent {


  password = "";
  constructor(public dialogRef: MatDialogRef<DmsDialogComponent>,private formBuilder: FormBuilder,
    private service: ServiceService,private dialog: MatDialog) {  
  }


  buttons = [
    { label: '1', command: 'button_1', color: '#3498db' },
    { label: '2', command: 'button_2', color: '#3498db'},
    { label: '3', command: 'button_3', color: '#3498db' },
    { label: 'A', command: 'button_A' , color: '#FF0000'},
    { label: '4', command: 'button_4', color: '#3498db' },
    { label: '5', command: 'button_5', color: '#3498db' },
    { label: '6', command: 'button_6' , color: '#3498db'},
    { label: 'B', command: 'button_B' , color: '#FF0000'},
    { label: '7', command: 'button_7', color: '#3498db' },
    { label: '8', command: 'button_8' , color: '#3498db'},
    { label: '9', command: 'button_9' , color: '#3498db'},
    { label: 'C', command: 'button_C' , color: '#FF0000'},
    { label: '*', command: 'button_*' , color: '#FF0000'},
    { label: '0', command: 'button_0' , color: '#3498db'},
    { label: '#', command: 'button_#' , color: '#FF0000'},
    { label: 'D', command: 'button_D' , color: '#FF0000'},
  ];

  onButtonClick(button: any): void {
    if (button.label ==='#'){
      this.service.dmsChangeDevice(this.password).subscribe({next:
        (response)=>{
          this.dialogRef.close(); 
        }, error: (error)=> {
          console.error(error)
        }})

    }else{
      this.password += button.label
    }
    
  }



  closeDialog(): void{
    this.dialogRef.close();

  }

}
