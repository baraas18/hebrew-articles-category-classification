import { useState } from 'react'
import TextField from '@mui/material/TextField'
// import InputLabel from '@mui/material/InputLabel'
import SendIcon from '@mui/icons-material/Send'
import LoadingButton from '@mui/lab/LoadingButton'
import { DataGrid } from '@mui/x-data-grid'
import { renderProgress } from './RenderProgress'
import './App.css'

function App() {
  const [text, setText] = useState('')
  const [rows, setRows] = useState([
    { id: '0', category: 'Sport - ספורט', confidence_percentage: 0 },
    { id: '1', category: 'Entertainment - תרבות', confidence_percentage: 0 },
    { id: '2', category: 'Economy - כלכלה', confidence_percentage: 0 },
    { id: '3', category: 'Health - בריאות', confidence_percentage: 0 },
    { id: '4', category: 'Car - רכב', confidence_percentage: 0 },
    { id: '5', category: 'Food - אוכל', confidence_percentage: 0 },
    { id: '6', category: 'Dating - יחסים', confidence_percentage: 0 },
    { id: '7', category: 'Parents - הורים', confidence_percentage: 0 }
  ])
  const [columns] = useState([
    { field: 'category', headerName: 'Category - קטגוריה', width: 180},
    {
      field: 'confidence_percentage',
      headerName: 'אחוז ודאות',
      renderCell: renderProgress,
      type: 'number',
      width: 200,
    }
  ])

  const [loading, setLoading] = useState(false)

  const handleClick = () => {
    setLoading(true)
    fetch('http://127.0.0.1:5000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(
        {
          'text': text
        }
      ),
    })
      .then(response => response.json())
      .then(data => {
        let newRows = []
        for (const key in data) {
          const value = data[key]
          newRows.push({ id: key, category: `${value['english']} - ${value['hebrew']}`, confidence_percentage: value['confidence_percentage'] })
        }
        setRows(newRows)
      })
      .catch((error) => {
        console.error('Error:', error)
      })
      .finally(() => {
        setLoading(false)
      })
  }

  return (
    <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
      <h1>סיווג טקסטים לפי קטגוריות</h1>
      <div style={{
        display: 'flex',
        alignItems: 'flex-start',
        justifyContent: 'space-around',
        width: '85%'
      }}>
        <div style={{ width: '40%', margin: '1%' }}>
          <DataGrid
            rows={rows}
            columns={columns}
            // autosizeOnMount
            hideFooter
            initialState={{
              sorting: {
                sortModel: [{ field: 'confidence_percentage', sort: 'desc' }],
              },
            }}
            style={{ width: '100%', height: '474px' }}
          />
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', width: '70%' }}>
          <TextField
            sx={{ '& label': { fontSize: '1.1rem', textAlign: 'right' } }} // Add textAlign: 'right' to align the label on the right
            placeholder='יש להזין את הטקסט...'
            multiline
            rows={20}
            dir='rtl'
            value={text}
            variant='outlined'
            onChange={(e) => setText(e.target.value)}
            style={{ width: '100%', margin: '1%' }}
            />
          <LoadingButton
            size='large'
            onClick={handleClick}
            startIcon={<SendIcon style={{ transform: 'scaleX(-1)' }}/>}
            loading={loading}
            loadingPosition='center'
            variant='contained'
            style={{ width: '100%', marginBottom: '2%' }}
            >
            <span>פענח</span>
          </LoadingButton>
        </div>
      </div>
    </div>
  )
}

export default App
