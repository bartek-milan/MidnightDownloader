D=print
F=False
C=True
import tkinter as J,time as G,threading as I,os,numpy as H,cv2
from PIL import ImageGrab as K
import tkinter.messagebox as L
M=100
N=50
E=20
B=15
O=300
class A:
	def __init__(A):N='bold';M='Arial';L='red';I='green';D='white';A.width=300;A.height=200;A.x=300;A.y=200;A.monitoring=F;A.shutdown_scheduled=F;A.root=J.Tk();A.root.title('Download Watcher');A.root.overrideredirect(C);A.root.attributes('-topmost',C);A.root.attributes('-transparentcolor',D);A.root.configure(bg=D);A.set_geometry();A.canvas=J.Canvas(A.root,width=A.width,height=A.height+B+20,bg=D,highlightthickness=0);A.canvas.pack();A.border_thickness=10;A.rect=A.canvas.create_rectangle(0,B,A.width,A.height+B,outline=I,width=A.border_thickness);A.top_border_line=A.canvas.create_line(0,B,A.width,B,fill=I,width=A.border_thickness);A.resize_handle=A.canvas.create_rectangle(A.width-E,A.height+B-E,A.width,A.height+B,fill=L,outline=L);A.close_button=J.Button(A.root,text='X',command=A.root.destroy,bg=L,fg=D,borderwidth=0,font=(M,10,N),cursor='hand2');A.close_button.place(x=A.width-25,y=B+5,width=20,height=20);A.start_button=J.Button(A.root,text='Start',command=A.start_monitoring,bg=I,fg=D,borderwidth=0,font=(M,10,N));A.start_button.place(x=5,y=B+5,width=50,height=20);O='Created by Milán Bartek';A.font=M,12,N;A.padding_x=8;A.padding_y=4;P=A.canvas.create_text(0,0,text=O,font=A.font,anchor='nw');K=A.canvas.bbox(P);A.canvas.delete(P);A.text_width=K[2]-K[0];A.text_height=K[3]-K[1];G=A.width//2;H=B//2;A.outer_rect_coords=G-A.text_width//2-A.padding_x-2,H-A.text_height//2-A.padding_y-2,G+A.text_width//2+A.padding_x+2,H+A.text_height//2+A.padding_y+2;A.inner_rect_coords=G-A.text_width//2-A.padding_x,H-A.text_height//2-A.padding_y,G+A.text_width//2+A.padding_x,H+A.text_height//2+A.padding_y;A.text_outer_border=A.canvas.create_rectangle(*A.outer_rect_coords,fill=I,outline=I,width=1);A.text_inner_border=A.canvas.create_rectangle(*A.inner_rect_coords,fill='black',outline=D,width=1);A.text_id=A.canvas.create_text(G,H,text=O,fill=D,font=A.font);A.resizing=F;A.moving=F;A.start_x=0;A.start_y=0;A.canvas.bind('<Button-1>',A.mouse_down);A.canvas.bind('<B1-Motion>',A.mouse_drag);A.canvas.bind('<ButtonRelease-1>',A.mouse_up)
	def set_geometry(A):C=A.height+B+20;A.root.geometry(f"{A.width}x{C}+{A.x}+{A.y}")
	def in_corner(A,x,y):return x>=A.width-E and y>=A.height+B-E
	def mouse_down(A,event):
		B=event;A.start_x=B.x_root;A.start_y=B.y_root
		if A.in_corner(B.x,B.y):A.resizing=C
		else:A.moving=C
	def mouse_drag(A,event):
		F=event;G=F.x_root-A.start_x;H=F.y_root-A.start_y
		if A.resizing:I=max(M,A.width+G);J=max(N,A.height+H);A.width=I;A.height=J;A.set_geometry();A.canvas.config(width=A.width,height=A.height+B+20);A.canvas.coords(A.rect,0,B,A.width,A.height+B);A.canvas.coords(A.top_border_line,0,B,A.width,B);A.canvas.coords(A.resize_handle,A.width-E,A.height+B-E,A.width,A.height+B);C=A.width//2;D=B//2;A.outer_rect_coords=C-A.text_width//2-A.padding_x-2,D-A.text_height//2-A.padding_y-2,C+A.text_width//2+A.padding_x+2,D+A.text_height//2+A.padding_y+2;A.canvas.coords(A.text_outer_border,*A.outer_rect_coords);A.inner_rect_coords=C-A.text_width//2-A.padding_x,D-A.text_height//2-A.padding_y,C+A.text_width//2+A.padding_x,D+A.text_height//2+A.padding_y;A.canvas.coords(A.text_inner_border,*A.inner_rect_coords);A.canvas.coords(A.text_id,C,D);A.close_button.place(x=A.width-25,y=B+5);A.start_button.place(x=5,y=B+5)
		elif A.moving:A.x+=G;A.y+=H;A.set_geometry()
		A.start_x=F.x_root;A.start_y=F.y_root
	def mouse_up(A,event):A.resizing=F;A.moving=F
	def capture_screenshot(A):C=A.x;D=A.y+B+20;E=A.x+A.width;F=A.y+B+20+A.height;G=K.grab(bbox=(C,D,E,F));I=G.convert('L');return H.array(I)
	def compare_images(F,img1,img2):A=cv2.absdiff(img1,img2);C=H.sum(A>10);E=A.size;B=C/E*100;D(f"Change: {B:.2f}%");return B
	def schedule_shutdown(A):
		if not A.shutdown_scheduled:A.shutdown_scheduled=C;D('Shutdown scheduled: your PC will shut down in 15 minutes.');L.showinfo('Shutdown Scheduled','Your PC will shut down in 15 minutes. \n Thank you for using my software ^^ ');G.sleep(900);os.system('shutdown /s /t 0')
	def monitor_loop(A):
		B=A.capture_screenshot();D('Baseline screenshot taken.')
		while A.monitoring and not A.shutdown_scheduled:
			G.sleep(O);C=A.capture_screenshot();E=A.compare_images(B,C)
			if E<2.:D('Download likely complete. Scheduling shutdown in 15 minutes...');A.schedule_shutdown();break
			else:B=C
	def start_monitoring(A):
		if not A.monitoring:A.monitoring=C;I.Thread(target=A.monitor_loop,daemon=C).start();D('Monitoring started.')
	def run(A):A.root.mainloop()
if __name__=='__main__':A().run()