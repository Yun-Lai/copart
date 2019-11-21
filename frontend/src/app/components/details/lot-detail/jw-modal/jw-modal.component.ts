import {Component, ElementRef, Input, OnDestroy, OnInit} from '@angular/core';
import {ModelService} from '../../../../utils/services/model.service';

@Component({
  selector: 'jw-modal',
  templateUrl: './jw-modal.component.html',
  styleUrls: ['./jw-modal.component.scss']
})
export class ModalComponent implements OnInit, OnDestroy {

  @Input() id: string;
  element: any;

  constructor(private modalService: ModelService, private el: ElementRef) {
    this.element = el.nativeElement;
  }

  ngOnInit() {
    let modal = this;

    if (!this.id) {
      console.error('modal must have an id');
      return;
    }

    document.body.appendChild(this.element);

    this.element.addEventListener('click', function(e: any) {
      if (e.target.className === 'jw-modal') {
        modal.close();
      }
    });
    this.modalService.add(this);
  }

  ngOnDestroy(): void {
    this.modalService.remove(this.id);
    this.element.remove();
  }

  open(): void {
    this.element.style.display = 'block';
    document.body.classList.add('jw-modal-open');
  }

  close(): void {
    this.element.style.display = 'none';
    document.body.classList.remove('jw-modal-open');
  }
}
